"""Synthetic host setup shared by Lite regression tests."""

from tests.native_adapter_support import FakeHostContext


def host_config(**changes):
    config = {
        "staging": {"enabled": True, "profile_id": "preview-1", "delivery_mode": "preview"},
        "target": {
            "platform_id": "qq-main",
            "account_id": "100",
            "participant_id": "200",
            "bot_id": "bot-a",
            "role_id": "persona-a",
            "persona_id": "original",
        },
        "model": {
            "provider_id": "native-model",
            "task_prompt": "保持原角色，只根据当前输入回复。",
            "max_output_tokens": 100,
            "maximum_input_estimate": 131072,
            "output_parameter": "max_tokens",
            "input_microusd_per_million": 2_000_000,
            "cached_input_microusd_per_million": 1_000_000,
            "output_microusd_per_million": 4_000_000,
        },
        "runtime": {
            "budget_tokens": 100_000_000,
            "budget_cost_microusd": 1_000_000_000,
            "quiet_seconds": 0,
            "maximum_wait_seconds": 0,
            "turn_timeout_seconds": 180,
            "part_gap_seconds": 0,
            "foreground_slots": 2,
            "background_slots": 1,
            "queued_per_lane": 64,
            "retained_tasks": 10000,
        },
    }
    for section, values in changes.items():
        config[section].update(values)
    return config


class WebContext(FakeHostContext):
    def __init__(self):
        super().__init__()
        self.registered_web_apis = []

    def register_web_api(self, route, handler, methods, description):
        for index, item in enumerate(self.registered_web_apis):
            if item[0] == route and item[2] == methods:
                self.registered_web_apis[index] = (route, handler, methods, description)
                return
        self.registered_web_apis.append((route, handler, methods, description))

    def get_using_provider(self, umo=None):
        return self.provider
