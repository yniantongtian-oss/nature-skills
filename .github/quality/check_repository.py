"""Check tracked checkout portability and package manifests without running project code."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path, PurePosixPath

WINDOWS_DEVICE = re.compile(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?$", re.I)
INVALID_CHARACTERS = re.compile(r'[<>:"\\|?*\x00-\x1f]')
MANIFESTS = {"package.json", "pyproject.toml", "Cargo.toml", "composer.json", "deno.json"}
FIXTURE_DIRS = {"fixture", "fixtures", "test", "tests", "testdata", "__fixtures__"}


def tracked(root: Path) -> list[str]:
    result = subprocess.check_output(
        ["git", "ls-tree", "-r", "-z", "--name-only", "HEAD"], cwd=root
    )
    return [item.decode("utf-8") for item in result.split(b"\0") if item]


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate object key: {key}")
        result[key] = value
    return result


def check(root: Path) -> dict:
    import tomllib

    paths = tracked(root)
    findings = []
    folded = {}
    manifests = 0
    for path in paths:
        parts = PurePosixPath(path).parts
        key = unicodedata.normalize("NFC", path).casefold()
        if key in folded and folded[key] != path:
            findings.append({"code": "case_collision", "path": path, "other": folded[key]})
        folded[key] = path
        for part in parts:
            if (
                INVALID_CHARACTERS.search(part)
                or part.endswith((".", " "))
                or WINDOWS_DEVICE.match(part)
            ):
                findings.append({"code": "windows_checkout_path", "path": path, "component": part})
                break
        if parts[-1] not in MANIFESTS or FIXTURE_DIRS.intersection(parts[:-1]):
            continue
        location = root / path
        payload = (
            location.read_bytes()
            if location.is_file()
            else subprocess.check_output(["git", "show", f"HEAD:{path}"], cwd=root)
        )
        try:
            text = payload.decode("utf-8-sig")
            data = (
                tomllib.loads(text)
                if path.endswith(".toml")
                else json.loads(text, object_pairs_hook=no_duplicate_keys)
            )
            if not isinstance(data, dict):
                raise ValueError("package manifest must be an object")
            manifests += 1
        except (UnicodeError, ValueError, tomllib.TOMLDecodeError) as exc:
            findings.append({"code": "invalid_manifest", "path": path, "message": str(exc)})
    exceptions_file = root / ".github/quality/exceptions.json"
    exceptions = (
        json.loads(exceptions_file.read_text(encoding="utf-8")) if exceptions_file.exists() else []
    )
    ignored, errors = [], []
    for finding in findings:
        exemption = next(
            (
                item
                for item in exceptions
                if item["code"] == finding["code"]
                and item["path"] == finding["path"]
                and item.get("reason")
            ),
            None,
        )
        (ignored if exemption else errors).append(finding)
    return {
        "tracked_files": len(paths),
        "valid_manifests": manifests,
        "errors": errors,
        "reviewed_exceptions": ignored,
        "scope": "Checkout paths and manifest syntax; not application tests",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    args = parser.parse_args()
    report = check(args.root.resolve())
    print(json.dumps({"ok": not report["errors"], "data": report}, ensure_ascii=False, indent=2))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
