"""Verify vendored skill dependency trees against the retained manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def tree_evidence(root: Path) -> dict:
    files = sorted((path for path in root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(root).as_posix())
    digest = hashlib.sha256()
    total = 0
    for path in files:
        data = path.read_bytes()
        total += len(data)
        relative = path.relative_to(root).as_posix()
        digest.update(f"{relative}\0{hashlib.sha256(data).hexdigest()}\n".encode("utf-8"))
    return {"files": len(files), "bytes": total, "tree_sha256": digest.hexdigest()}


def audit(root: Path = ROOT, manifest_name: str = "external-skill-dependencies.json") -> list[dict]:
    manifest = json.loads((root / manifest_name).read_text(encoding="utf-8"))
    if manifest.get("schema") != "workflowmoves.external-skill-dependencies.v2":
        raise ValueError("Unexpected dependency manifest schema")
    results = []
    for dependency in manifest["dependencies"]:
        status = dependency["copy_status"]
        if status == "vendored":
            path = (root / dependency["vendored_path"]).resolve()
            if not path.is_relative_to(root.resolve()) or not path.is_dir():
                raise ValueError(f"Missing or escaping vendored dependency: {dependency['id']}")
            actual = tree_evidence(path)
            expected = {key: dependency[key] for key in ("files", "bytes", "tree_sha256")}
            if actual != expected:
                raise ValueError(f"Vendored dependency mismatch for {dependency['id']}: {actual} != {expected}")
            if not any((path / name).is_file() for name in ("LICENSE.txt", "license.txt", "LICENSE")):
                raise ValueError(f"Vendored dependency has no retained licence: {dependency['id']}")
        elif status.startswith("blocked_"):
            if dependency.get("vendored_path"):
                raise ValueError(f"Blocked dependency unexpectedly declares vendored_path: {dependency['id']}")
            if not dependency.get("blocker"):
                raise ValueError(f"Blocked dependency has no reason: {dependency['id']}")
        else:
            raise ValueError(f"Unknown copy_status for {dependency['id']}: {status}")
        results.append({"id": dependency["id"], "status": status})
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    options = parser.parse_args()
    results = audit(options.root.resolve())
    print(json.dumps({"dependencies": len(results), "states": {state: sum(row["status"] == state for row in results) for state in sorted({row["status"] for row in results})}}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
