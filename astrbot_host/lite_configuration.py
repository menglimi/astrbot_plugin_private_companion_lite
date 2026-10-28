"""Apply administrator-owned plugin settings through the core configuration service."""

import json
from uuid import uuid4

from companion_v2.configuration.models import ConfigLayer, ConfigTarget
from companion_v2.execution.models import TaskError, require
from companion_v2.foundation.refs import OperationRef, SubjectKind, SubjectRef, VersionRef
from companion_v2.identity_policy.models import AuthenticatedHostPrincipal, AuthorizationTier
from companion_v2.identity_policy.object_access import ObjectAccessPolicy
from companion_v2.identity_policy.repository import PersistentIdentityDirectory
from .group_settings import GroupTarget


def _operator(runtime, at):
    """This identity represents saved host configuration, never chat input."""
    principal = AuthenticatedHostPrincipal(runtime.installation_id, "astrbot-plugin-config",
                                          "lite", "core-preferences")
    identities = PersistentIdentityDirectory(runtime)
    result = identities.resolve_authenticated(principal, observed_at=at)
    if result.failure is not None and result.failure.code == "unbound_identity":
        subject = SubjectRef(runtime.installation_id, SubjectKind.SERVICE, "lite-plugin-config")
        identities.bind(binding_id="lite-plugin-config", principal=principal, subject=subject,
                        valid_from=at, expected_revision=identities.revision)
        policy = ObjectAccessPolicy(runtime)
        policy.set_tier(subject, AuthorizationTier.CORE, expected_revision=policy.revision, observed_at=at)
        result = identities.resolve_authenticated(principal, observed_at=at)
    return require(result)


def _changes(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"重复字段：{key}")
            result[key] = value
        return result

    value = json.loads(raw, object_pairs_hook=unique,
                       parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
    if type(value) is not dict:
        raise ValueError("设置值必须为 JSON 对象")
    return value


def apply_core_preferences(controller):
    """Validate and commit the complete form atomically before starting workers.

    Only listed fields are touched. Removing an entry preserves stored values;
    reset_to_inherit explicitly removes an override. Repeated reloads are no-ops
    when the same values are already present.
    """
    section = controller.config.get("core_preferences", {})
    if not isinstance(section, dict):
        raise TaskError("lite_configuration_invalid", "核心偏好必须为配置对象")
    entries = section.get("entries", [])
    if type(entries) is not list:
        raise TaskError("lite_configuration_invalid", "核心偏好条目必须为列表")
    if not entries:
        return
    app = controller.session.application
    at = controller.now()
    try:
        with app.runtime.transaction():
            actor = _operator(app.runtime, at)
            seen = set()
            for index, entry in enumerate(entries, 1):
                if type(entry) is not dict:
                    raise ValueError(f"第 {index} 项必须为配置对象")
                group = entry.get("group_id", "")
                definitions = app.configuration.registry.group(group)
                layer = ConfigLayer(entry.get("layer", "role"))
                if layer not in definitions[0].layers:
                    raise ValueError(f"{group} 不支持 {layer.value} 层级，请查看字段参考")
                if layer is ConfigLayer.INSTALLATION:
                    target = ConfigTarget(app.runtime.installation_id, layer)
                elif layer is ConfigLayer.ROLE:
                    configured = controller.settings.target(entry.get("target_id", ""))
                    role_id = controller.settings.canonical_role_id(entry.get("role_id", ""))
                    if configured is None or not any(mapping.bot_id == configured.bot_id
                            and mapping.role_id == role_id for mapping in controller.settings.personas):
                        raise ValueError("角色范围需要已配置的目标和对应人格映射")
                    target = ConfigTarget(app.runtime.installation_id, layer,
                        role=SubjectRef(app.runtime.installation_id, SubjectKind.BOT, role_id),
                        bot_id=configured.bot_id)
                else:
                    if isinstance(controller.settings.target(entry.get("target_id", "")), GroupTarget):
                        raise ValueError("Lite 群聊偏好请使用 role 范围和群目标对应的角色 ID")
                    context = controller.authority.context(entry.get("target_id", ""), entry.get("role_id", ""))
                    target = ConfigTarget(app.runtime.installation_id, layer,
                        role=context.role_binding.role if layer is not ConfigLayer.SCOPE else None,
                        scope=context.scope if layer in (ConfigLayer.WINDOW, ConfigLayer.SCOPE) else None,
                        bot_id=context.scope.bot_id,
                        subject=context.actor.subject if layer in (ConfigLayer.WINDOW, ConfigLayer.RELATIONSHIP) else None)
                key = target.key, group
                if key in seen:
                    raise ValueError(f"{group} 在同一范围内重复，请合并为一项")
                seen.add(key)
                changes = _changes(entry.get("values", "{}"))
                reset = entry.get("reset_to_inherit", [])
                if type(reset) is not list or any(type(name) is not str for name in reset):
                    raise ValueError("恢复继承字段必须为字符串列表")
                snapshot = require(app.configuration.read(actor, target=target, group_id=group, observed_at=at))
                # Use normal validation even if all values appear unchanged.
                require(app.configuration.preview_changes(actor, target=target, group_id=group,
                    changes=changes, observed_at=at))
                if not reset and all(snapshot.fields[name].value == value
                                     and snapshot.fields[name].source == target for name, value in changes.items()):
                    continue
                identifier = "lite-config-" + uuid4().hex
                operation = OperationRef(identifier, definitions[0].owner_id, target.authorization_scope,
                                         VersionRef(identifier, 1), identifier)
                require(app.configuration.patch(actor, target=target, group_id=group,
                    operation=operation, expected_edit_token=snapshot.edit_token,
                    changes=changes, reset_to_inherit=tuple(reset), observed_at=at))
    except (TypeError, ValueError, KeyError, TaskError) as error:
        raise TaskError("lite_configuration_invalid", f"核心偏好未应用：{error}") from error
