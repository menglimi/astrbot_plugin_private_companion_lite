"""Packaging prevents credentials, runtime data and full-edition feature leakage."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tools.build_v2_release import allowed, checked_payload, validate_edition, ROOT


class LiteReleaseTests(unittest.TestCase):
    def test_edition_contract(self):
        validate_edition(ROOT)

    def test_excludes_data_and_full_edition(self):
        root = Path("root")
        for path in ("data/runtime.db", "pages/陪伴小屋/index.html",
                     "astrbot_host/native_extensions/image.py", "companion_v2/screen/peek.py"):
            self.assertFalse(allowed(root / path, root), path)

    def test_rejects_credentials_without_echoing_them(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "example.txt"
            for prefix in ("ghp_", "github_pat_", "abk_", "sk-proj-"):
                source.write_text(prefix + "x" * 48, encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "credential-like content rejected"):
                    checked_payload(source, root)


if __name__ == "__main__":
    unittest.main()
