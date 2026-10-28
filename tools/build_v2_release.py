"""Build the standalone 7.0.0lite archive; never traverse runtime data."""

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import zipfile


ROOT = Path(__file__).resolve().parents[1]
CORE_ID = "astrbot_plugin_private_companion"
VERSION = "7.0.0+lite"
CORE_DIRS = ("astrbot_host", "companion_v2", "tests", "tools", "docs", "fixtures")
ROOT_FILES = {"main.py", "metadata.yaml", "_conf_schema.json", "requirements.txt", "pyproject.toml",
              "README.md", "CHANGELOG.md", "logo.png", "pytest.ini"}
EXCLUDED = {"data", "__pycache__", ".git", ".pytest_cache", "build", "dist", "node_modules", "verification"}
REMOVED = ("pages", "astrbot_host/native_extensions", "astrbot_host/huawei_health",
           "companion_v2/content", "companion_v2/games", "companion_v2/live", "companion_v2/reality",
           "companion_v2/screen", "companion_v2/together", "companion_v2/conversation/content")
TEXT_SUFFIXES = {".py", ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".ini", ".sql", ".csv"}
SECRET_PATTERNS = [
    re.compile(rb"(?<![A-Za-z0-9])gh[pousr]_[A-Za-z0-9_]{30,}"),
    re.compile(rb"(?<![A-Za-z0-9])github_pat_[A-Za-z0-9_]{30,}"),
    re.compile(rb"(?<![A-Za-z0-9])abk_[A-Za-z0-9_-]{30,}"),
    re.compile(rb"(?<![A-Za-z0-9])sk-(?:proj-)?[A-Za-z0-9_-]{32,}"),
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]


def digest(payload):
    return hashlib.sha256(payload).hexdigest()


def allowed(path, root):
    relative = path.relative_to(root)
    name = relative.as_posix()
    return (not path.is_symlink() and not any(part in EXCLUDED for part in relative.parts)
            and not any(name == item or name.startswith(item + "/") for item in REMOVED)
            and path.suffix not in {".pyc", ".db", ".sqlite", ".sqlite3", ".log", ".out", ".bak", ".backup"}
            and not any(part.startswith(".env") or "design-preview" in part for part in relative.parts))


def sources(root, directories=CORE_DIRS):
    selected = [root / name for name in ROOT_FILES if (root / name).is_file()]
    for directory in directories:
        for base, children, files in os.walk(root / directory, followlinks=False):
            children[:] = sorted(name for name in children if allowed(Path(base) / name, root))
            selected.extend(Path(base) / name for name in sorted(files) if allowed(Path(base) / name, root))
    return sorted(selected, key=lambda path: path.relative_to(root).as_posix())


def checked_payload(path, root):
    payload = path.read_bytes()
    if any(pattern.search(payload.replace(b"\\n", b"\n")) for pattern in SECRET_PATTERNS):
        raise ValueError("credential-like content rejected in " + str(path.relative_to(root)))
    if path.suffix in TEXT_SUFFIXES:
        text = payload.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n"
        if path.suffix == ".py":
            ast.parse(text, filename=str(path.relative_to(root)))
        payload = text.encode("utf-8")
    return payload


def validate_edition(root):
    for relative in REMOVED:
        if (root / relative).exists():
            raise ValueError("Lite must not contain " + relative)
    metadata = (root / "metadata.yaml").read_text(encoding="utf-8")
    if f"version: {VERSION}\n" not in metadata or f"name: {CORE_ID}\n" not in metadata:
        raise ValueError("Lite metadata identity/version mismatch")
    product = (root / "companion_v2/product/__init__.py").read_text(encoding="utf-8")
    if f'PRODUCT_VERSION = "{VERSION}"' not in product:
        raise ValueError("Lite product version mismatch")
    if f'version = "{VERSION}"' not in (root / "pyproject.toml").read_text(encoding="utf-8"):
        raise ValueError("Lite build version mismatch")
    schema = json.loads((root / "_conf_schema.json").read_text(encoding="utf-8"))
    if schema["multi_host"].get("invisible", False) or "core_preferences" not in schema:
        raise ValueError("Lite requires usable official configuration")


def build(output, root=ROOT):
    validate_edition(root)
    output = output.resolve()
    if output == root.resolve() or output.is_relative_to(root.resolve()):
        raise ValueError("release output must be outside the source tree")
    output.mkdir(parents=True, exist_ok=True)
    archive = output / (CORE_ID + "-7.0.0lite.zip")
    if archive.exists():
        raise FileExistsError(archive)
    inventory = {}
    with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for path in sources(root):
            name = path.relative_to(root).as_posix()
            payload = checked_payload(path, root)
            inventory[name] = digest(payload)
            info = zipfile.ZipInfo(CORE_ID + "/" + name, date_time=(2026, 10, 29, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, payload)
    manifest = {"schema": "companion.lite.release.v1", "version": VERSION, "branch": "7.0.0lite",
                "archive": archive.name, "sha256": digest(archive.read_bytes()), "files": inventory}
    (output / "release.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                                       encoding="utf-8", newline="\n")
    return {"archive": str(archive), "sha256": manifest["sha256"], "files": len(inventory),
            "bytes": archive.stat().st_size}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    print(json.dumps(build(arguments.output), ensure_ascii=False))
