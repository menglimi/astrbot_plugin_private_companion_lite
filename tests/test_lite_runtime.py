"""Lite starts core domains without pages or bundled extension providers."""

import json
from dataclasses import replace
from pathlib import Path
import sys
import unittest

from tests.multi_host_support import MultiFixture, multi_config
from astrbot_host.lite_configuration import apply_core_preferences
from companion_v2.execution.models import TaskError


REMOVED = ("content.", "image.generate", "image.edit", "image.mask_edit", "screen.",
           "reality.", "together.", "game.", "live.")


class LiteRuntimeTests(MultiFixture, unittest.IsolatedAsyncioTestCase):
    async def test_core_start_reply_memory_and_stop_without_extensions(self):
        app = await self.start_host()
        self.assertEqual(self.native.registered_web_apis, [])
        self.assertIsNone(self.controller.session.native_tool_port)
        context, batch = await self.accepted(text="我不喝咖啡")
        self.assertTrue(app.messages.batch(batch))
        self.remember(app, context, batch)
        actions = [tool.action for tool in app.tools.catalog_for(context)]
        self.assertTrue(actions)
        self.assertFalse([action for action in actions if action.startswith(REMOVED)])
        self.assertFalse([name for name in sys.modules if '.native_extensions' in name
                          or name.startswith(('companion_v2.screen', 'companion_v2.games',
                              'companion_v2.reality', 'companion_v2.live', 'companion_v2.content',
                              'companion_v2.together', 'companion_v2.conversation.content'))])
        await self.controller.terminate()
        self.assertIsNone(self.controller.runtime)
        self.assertEqual(app.state, "stopped")
        self.assertFalse(app.active_handles)

    async def test_core_configuration_is_validated_and_atomic(self):
        self.controller.config["core_preferences"] = {"entries": [
            {"group_id": "private_access", "layer": "installation",
             "values": '{"private_access.proactive_default": true}'}]}
        app = await self.start_host()
        fields = app.configuration.registry.group("proactive.contact")
        flag = next(field for field in fields if field.field_id == "proactive.contact.enabled")
        entry = {"group_id": flag.group_id, "layer": "installation",
                 "values": json.dumps({flag.field_id: not flag.default})}
        self.controller.config["core_preferences"] = {"entries": [entry]}
        apply_core_preferences(self.controller)
        context = self.controller.authority.context("first", "role-a")
        self.controller.authority.provision_scope(self.controller.settings.target("first"),
                                                 context.scope, context.role_binding.role)
        preferences = app.proactive.preferences.read(context, observed_at=self.clock.now()).unwrap()
        self.assertEqual(preferences.values["enabled"], not flag.default)
        before = app.runtime.read_all("SELECT * FROM configuration_changes", ())
        apply_core_preferences(self.controller)
        self.assertEqual(before, app.runtime.read_all("SELECT * FROM configuration_changes", ()))
        self.controller.config["core_preferences"]["entries"] = [
            {**entry, "values": json.dumps({flag.field_id: flag.default})},
            {"group_id": "missing.lite.group", "values": "{}"}]
        with self.assertRaises(TaskError):
            apply_core_preferences(self.controller)
        self.assertEqual(before, app.runtime.read_all("SELECT * FROM configuration_changes", ()))
        self.controller.config["core_preferences"]["entries"] = [{**entry,
            "values": "{}", "reset_to_inherit": [flag.field_id]}]
        apply_core_preferences(self.controller)
        preferences = app.proactive.preferences.read(context, observed_at=self.clock.now()).unwrap()
        self.assertEqual(preferences.values["enabled"], flag.default)

    async def test_role_preferences_reach_the_role_consumer(self):
        app = await self.start_host()
        from astrbot_host.group_settings import GroupTarget
        self.controller.settings = replace(self.controller.settings,
            group_targets=(GroupTarget("group-1", "qq-main", "100", "bot-a", "300"),))
        entry = {"group_id": "conversation.perception", "layer": "role",
                 "target_id": "group-1", "role_id": "role-a",
                 "values": json.dumps({"conversation.perception.guidance": "留意当前时段，自然回应。"})}
        # Field IDs are defined by the domain, not inferred from UI labels.
        field = next(f for f in app.configuration.registry.group(entry["group_id"])
                     if f.field_id.endswith(".guidance"))
        entry["values"] = json.dumps({field.field_id: "留意当前时段，自然回应。"})
        self.controller.config["core_preferences"] = {"entries": [entry]}
        apply_core_preferences(self.controller)
        context = self.controller.authority.context("first", "role-a")
        self.assertEqual(app.perception_settings.capture(context, self.clock.now())["settings"]["guidance"],
                         "留意当前时段，自然回应。")
    async def test_invalid_form_prevents_partial_start(self):
        config = multi_config()
        config["core_preferences"] = {"entries": [{"group_id": "missing.lite.group", "values": "{}"}]}
        self.controller = self.make_controller(config)
        result = await self.controller.start()
        self.assertFalse(result.is_success)
        self.assertEqual(result.failure.code, "lite_configuration_invalid")
        self.assertFalse(self.controller._accepting)
        retried = await self.controller.start()
        self.assertFalse(retried.is_success)
        self.assertEqual(retried.failure.code, "lite_configuration_invalid")


class LitePackageTests(unittest.TestCase):
    def test_help_does_not_direct_people_to_removed_pages(self):
        from astrbot_host.functional_commands import FunctionalCommand, command_instruction
        for intent in ("help", "manage_contact", "manage_life", "image_generate", "manage_native"):
            instruction = command_instruction(FunctionalCommand("private", intent))
            self.assertNotIn("陪伴小屋", instruction)
        self.assertIn("未包含", command_instruction(FunctionalCommand("private", "image_generate")))

    def test_no_pages_or_bundled_implementations(self):
        root = Path(__file__).resolve().parents[1]
        for relative in ("pages", "astrbot_host/native_extensions", "astrbot_host/huawei_health",
                         "companion_v2/content", "companion_v2/games", "companion_v2/live",
                         "companion_v2/reality", "companion_v2/screen", "companion_v2/together",
                         "companion_v2/conversation/content"):
            self.assertFalse((root / relative).exists(), relative)
        schema = json.loads((root / "_conf_schema.json").read_text(encoding="utf-8"))
        self.assertFalse(schema["multi_host"].get("invisible", False))
        self.assertIn("core_preferences", schema)
        self.assertNotIn("performance", schema)
        requirements = (root / "requirements.txt").read_text(encoding="utf-8")
        for dependency in ("sounddevice", "soundfile", "opencv", "mijia", "fastmcp", "numpy"):
            self.assertNotIn(dependency, requirements)


if __name__ == "__main__":
    unittest.main()
