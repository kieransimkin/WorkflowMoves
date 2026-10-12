"""Apply this package's additive workflow routes without replacing existing files."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def contained(root: Path, relative: str) -> Path:
    target = (root / relative).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError(f"Path leaves workspace: {relative}")
    return target


def merge(text: str, snippet: str, anchor: str, identity: str, newline: str = "\n") -> str:
    normalized_text = text.replace("\r\n", "\n")
    normalized_snippet = snippet.replace("\r\n", "\n")
    if normalized_snippet in normalized_text:
        if normalized_text.count(normalized_snippet) != 1:
            raise ValueError(f"Duplicate managed block: {identity}")
        return text
    if identity in text:
        raise ValueError(f"Existing managed block differs: {identity}")
    if text.count(anchor) != 1:
        raise ValueError(f"Missing or ambiguous anchor: {anchor}")
    return text.replace(anchor, snippet.rstrip() + newline * 2 + anchor, 1)


def plan(root: Path, package: Path = PACKAGE) -> list[dict]:
    routes = json.loads((package / "routes.json").read_text(encoding="utf-8"))
    changes = []
    seen = {}
    for row in routes:
        target = contained(root, row["target"])
        before = seen.get(target, target.read_bytes() if target.exists() else b"")
        source = contained(package, row["source"]).read_bytes()
        if row["mode"] == "copy":
            if before and before != source and not (row.get('previous_source') and before == contained(package, row['previous_source']).read_bytes()):
                raise ValueError(f"Existing destination differs: {row['target']}")
            after = source
        else:
            if not before:
                raise ValueError(f"Existing workflow missing: {row['target']}")
            # Retain newline style and BOM; preserve all non-managed text.
            has_bom = before.startswith(b"\xef\xbb\xbf")
            old = before.decode("utf-8-sig")
            newline = "\r\n" if "\r\n" in old else "\n"
            snippet = source.decode("utf-8-sig").replace("\r\n", "\n").strip().replace("\n", newline)
            previous = row.get("previous_source")
            prior = contained(package, previous).read_text(encoding="utf-8-sig").replace("\r\n", "\n").strip().replace("\n", newline) if previous else None
            if prior and snippet not in old and old.count(prior) == 1 and old.count(row["identity"]) == 1:
                updated = old.replace(prior, snippet, 1)
            else:
                updated = merge(old, snippet, row["anchor"], row["identity"], newline)
            after = (b"\xef\xbb\xbf" if has_bom else b"") + updated.encode("utf-8")
        seen[target] = after
        changes.append({"target": str(target), "before": before, "after": after})
    # Combine multiple routes for one file, preserving the original guard.
    combined = {}
    for item in changes:
        if item["target"] not in combined:
            combined[item["target"]] = dict(item)
        else:
            combined[item["target"]]["after"] = item["after"]
    return list(combined.values())


def install(root: Path, package: Path = PACKAGE, check: bool = False) -> list[dict]:
    changes = plan(root, package)
    results = []
    for item in changes:
        target = Path(item["target"])
        current = target.read_bytes() if target.exists() else b""
        if current != item["before"]:
            raise ValueError(f"Concurrent source change: {target}")
        changed = item["before"] != item["after"]
        if changed and not check:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(item["after"])
            if target.read_bytes() != item["after"]:
                raise ValueError(f"Readback mismatch: {target}")
        results.append({"target": str(target), "status": "pending" if changed and check else "updated" if changed else "current", "before_sha256": digest(item["before"]), "after_sha256": digest(item["after"])})
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--record", type=Path)
    options = parser.parse_args()
    records = install(options.root, check=options.check)
    serialized = json.dumps(records, indent=2)
    if options.record:
        options.record.parent.mkdir(parents=True, exist_ok=True)
        options.record.write_text(serialized + "\n", encoding="utf-8")
    print(json.dumps({"targets": len(records), "states": {s: sum(r["status"] == s for r in records) for s in ("updated", "current", "pending")}}))
