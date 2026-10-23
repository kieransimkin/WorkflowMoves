"""Check maintained workflow coverage, not runtime acceptance or chat completeness."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

SCHEMA = "workflowmoves.tool-workflows.v1"


def local_file(root: Path, value: object) -> bool:
    if not isinstance(value, str) or not value or ":" in value or "\\" in value:
        return False
    candidate = (root / value).resolve()
    return candidate.is_relative_to(root.resolve()) and candidate.is_file()


def validate(data: object, root: Path) -> dict:
    errors: list[str] = []
    if not isinstance(data, dict) or data.get("schema") != SCHEMA:
        return {"valid": False, "errors": ["unsupported workflow-map schema"]}
    try:
        index = (root / "workflows/danceflow/capabilities/index.md").read_text(encoding="utf-8")
        indexed = re.findall(r"^\| \[[^\]]+\]\(([a-z0-9-]+)\.md\)", index, re.M)
        members = set(indexed)
    except OSError:
        return {"valid": False, "errors": ["capability membership index unavailable"]}
    if not members:
        errors.append("capability membership index is empty")
    if len(indexed) != len(members):
        errors.append("capability membership index contains duplicate components")
    expected = members | {"toolkit"}
    rows = data.get("tools")
    if not isinstance(rows, list):
        return {"valid": False, "errors": ["tools must be a list"]}
    seen: set[str] = set()
    result = []
    for position, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"tool row {position} must be an object")
            continue
        identity = row.get("id")
        if not isinstance(identity, str) or identity not in expected or identity in seen:
            errors.append(f"unknown or duplicate tool: {identity}")
            continue
        seen.add(identity)
        if row.get("role") != ("toolkit" if identity == "toolkit" else "component"):
            errors.append(f"{identity}: incorrect membership role")
        reference = f"workflows/danceflow/capabilities/{identity}.md"
        if row.get("capabilities") != reference or not local_file(root, reference):
            errors.append(f"{identity}: missing canonical capability reference")
        routes = row.get("workflows")
        if not isinstance(routes, list) or not routes or any(not local_file(root, item) or not item.startswith("workflows/") or not item.endswith(".md") for item in routes):
            errors.append(f"{identity}: missing or unsafe workflow route")
        if not isinstance(row.get("task"), str) or not row["task"].strip():
            errors.append(f"{identity}: missing actual task")
        for field in ("inputs", "outputs", "acceptance", "limits"):
            values = row.get(field)
            if not isinstance(values, list) or not values or any(not isinstance(item, str) or not item.strip() for item in values):
                errors.append(f"{identity}: {field} must name concrete nonempty contracts")
        result.append({"id": identity, "role": row.get("role"), "workflow_routes": len(routes) if isinstance(routes, list) else 0})
    if seen != expected:
        errors.append("membership mismatch: missing=" + ",".join(sorted(expected-seen)))
    return {"valid": not errors, "component_count": len(members), "toolkit_count": int("toolkit" in seen),
            "tools": result, "errors": errors,
            "scope": "Documentation membership, local routes and retained contracts only; no execution, external-link, host, chat-history or public-output acceptance."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, nargs="?", default=Path(__file__).resolve().parents[1]/"docs/tool-workflow-map.json")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        report = validate(json.loads(args.path.read_text(encoding="utf-8-sig")), args.root)
    except (OSError, ValueError) as exc:
        report = {"valid": False, "errors": [str(exc)]}
    print(json.dumps(report, indent=2))
    return int(not report["valid"])


if __name__ == "__main__":
    raise SystemExit(main())
