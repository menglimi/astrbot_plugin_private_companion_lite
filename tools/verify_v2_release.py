"""Verify archive hashes and run the selected regressions from the extracted Lite package."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile

try:
    from .build_v2_release import CORE_ID, checked_payload, digest, validate_edition
except ImportError:
    from build_v2_release import CORE_ID, checked_payload, digest, validate_edition


def verify(release, extract_to, *, sdk=None, run_tests=False):
    manifest = json.loads((release / "release.json").read_text(encoding="utf-8"))
    archive = release / manifest["archive"]
    if digest(archive.read_bytes()) != manifest["sha256"]:
        raise ValueError("archive digest mismatch")
    if extract_to.exists():
        raise FileExistsError("verification destination must be new: " + str(extract_to))
    extract_to.mkdir(parents=True)
    expected = {CORE_ID + "/" + name for name in manifest["files"]}
    with zipfile.ZipFile(archive) as bundle:
        if set(bundle.namelist()) != expected or len(bundle.namelist()) != len(expected):
            raise ValueError("archive inventory mismatch")
        for name in bundle.namelist():
            target = (extract_to / name).resolve()
            if not target.is_relative_to(extract_to.resolve()):
                raise ValueError("archive path escapes destination")
        bundle.extractall(extract_to)
    root = extract_to / CORE_ID
    for name, expected_hash in manifest["files"].items():
        path = root / name
        if digest(path.read_bytes()) != expected_hash or checked_payload(path, root) != path.read_bytes():
            raise ValueError("file digest or encoding mismatch: " + name)
    validate_edition(root)
    result = {"archive_verified": True, "files": len(expected), "extracted_root": str(root)}
    if run_tests:
        environment = os.environ.copy()
        environment["PYTHONPATH"] = os.pathsep.join([str(root)] + ([str(sdk)] if sdk else []))
        temporary = extract_to / "isolated-runtime"
        temporary.mkdir()
        environment.update(PYTHONUTF8="1", TEMP=str(temporary), TMP=str(temporary),
                           ASTRBOT_ROOT=str(temporary / "astrbot"))
        log = release / "verification.log"
        with log.open("w", encoding="utf-8", newline="\n") as stream:
            completed = subprocess.run([sys.executable, "-X", "utf8", "-m", "tools.test_lite_release"],
                cwd=root, env=environment, stdout=stream, stderr=subprocess.STDOUT, timeout=900)
        if completed.returncode:
            raise RuntimeError("packaged regression failed; see " + str(log))
        result.update(tests_passed=True, log=str(log))
    (release / "verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                                              encoding="utf-8", newline="\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--release", type=Path, required=True)
    parser.add_argument("--extract-to", type=Path, required=True)
    parser.add_argument("--sdk", type=Path)
    parser.add_argument("--run-tests", action="store_true")
    args = parser.parse_args()
    print(json.dumps(verify(args.release, args.extract_to, sdk=args.sdk, run_tests=args.run_tests), ensure_ascii=False))
