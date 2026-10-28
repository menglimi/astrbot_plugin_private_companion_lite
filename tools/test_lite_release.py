"""One focused suite for the Lite composition, core behavior and SDK lifecycle."""

import unittest

TEST_MODULES = (
    "tests.test_lite_runtime",
    "tests.test_astrbot_plugin_reload",
    "tests.test_astrbot_core_reply",
    "tests.test_core_reply_reload",
    "tests.test_core_reply_voice",
    "tests.test_core_reply_voice_authoring",
    "tests.test_voice_reply",
    "tests.test_voice_language_command",
    "tests.test_private_debounce",
    "tests.test_reply_segmentation",
    "tests.test_memory_query",
    "tests.test_proactive_preferences",
    "tests.test_proactive_contacts",
    "tests.test_lite_release",
)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
