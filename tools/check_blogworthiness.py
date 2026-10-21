"""Validate retained editorial assessment completeness; never infer publication."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

STATES = {"covered", "prepared", "draft", "scheduled", "published", "verified_live", "blocked"}


def validate(record: dict) -> list[str]:
    if not isinstance(record, dict):
        return ["assessment must be an object"]
    errors = []
    for key in ("task", "reason"):
        if not isinstance(record.get(key), str) or not record[key].strip():
            errors.append(f"missing {key}")
    decision = record.get("decision")
    if decision not in {"PASS", "FAIL"}:
        errors.append("decision must be PASS or FAIL")
    evidence = record.get("evidence")
    if not isinstance(evidence, list) or not evidence or any(not isinstance(x, str) or not x.strip() for x in evidence):
        errors.append("evidence must be a nonempty list of source references")
    if decision == "PASS":
        for key in ("angle", "duplicate_check", "next_action"):
            if not isinstance(record.get(key), str) or not record[key].strip():
                errors.append(f"passing story needs {key}")
        state = record.get("state")
        if state not in STATES:
            errors.append("passing story needs a supported delivery state")
        if state == "blocked" and not str(record.get("blocker", "")).strip():
            errors.append("blocked story needs the exact blocker")
        if state in {"covered", "scheduled", "published", "verified_live"} and not str(record.get("url", "")).strip():
            errors.append("coverage/publication state needs a URL")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.path.read_text(encoding="utf-8-sig"))
        records = data if isinstance(data, list) else [data]
        failures = [{"index": i, "errors": errors} for i, r in enumerate(records) if (errors := validate(r))]
        if not records:
            failures.append({"errors": ["assessment list must not be empty"]})
        print(json.dumps({"valid": not failures, "count": len(records), "failures": failures,
                          "scope": "Record completeness only; no editorial, rights or public-output verification."}))
        return int(bool(failures))
    except (OSError, ValueError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
