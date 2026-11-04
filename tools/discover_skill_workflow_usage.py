"""Bounded inventory of reusable skills/workflows and their observed project use.

The scanner intentionally has no implicit search roots. Every catalogue and usage
location must be named in a reviewed manifest, and each location has independent
depth/file limits in addition to global file/byte budgets.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

SCHEMA = "workflowmoves.skill-workflow-scan.v1"
DEFAULT_EXCLUDES = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".venv",
    "node_modules",
    "models",
    "release",
    "previous",
    ".cache",
}


class ScanStopped(RuntimeError):
    """Raised after a hard budget is reached; the partial report is retained."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(path: str | Path, base: Path) -> Path:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = base / candidate
    return candidate.resolve(strict=False)


def is_within(path: Path, roots: Iterable[Path]) -> bool:
    return any(path == root or path.is_relative_to(root) for root in roots)


def is_link_or_junction(path: Path) -> bool:
    if path.is_symlink():
        return True
    checker = getattr(os.path, "isjunction", None)
    return bool(checker and checker(path))


def validate_scan_root(path: Path, *, workspace_root: Path, allowed_roots: list[Path]) -> None:
    if not path.is_absolute():
        raise ValueError(f"Scan root is not absolute: {path}")
    if path == Path(path.anchor):
        raise ValueError(f"Drive/filesystem root is forbidden: {path}")
    if path == workspace_root:
        raise ValueError(f"Workspace-root traversal is forbidden: {path}")
    if allowed_roots and not is_within(path, allowed_roots):
        raise ValueError(f"Scan root is outside allowed_roots: {path}")
    if is_link_or_junction(path):
        raise ValueError(f"Scan root may not be a link or junction: {path}")


def iter_bounded_files(
    root: Path,
    *,
    patterns: list[str],
    max_depth: int,
    excludes: set[str],
    max_files: int,
    skipped: list[dict],
):
    """Yield matching files without following links or walking beyond limits."""
    stack: list[tuple[Path, int]] = [(root, 0)]
    yielded = 0
    while stack:
        folder, depth = stack.pop()
        try:
            entries = sorted(os.scandir(folder), key=lambda item: item.name.casefold())
        except OSError as exc:
            skipped.append({"path": str(folder), "reason": "directory_unreadable", "detail": str(exc)})
            continue
        for entry in entries:
            path = Path(entry.path)
            if entry.name in excludes:
                skipped.append({"path": str(path), "reason": "excluded_name"})
                continue
            try:
                linked = entry.is_symlink() or is_link_or_junction(path)
                if linked:
                    skipped.append({"path": str(path), "reason": "link_or_junction"})
                    continue
                if entry.is_dir(follow_symlinks=False):
                    if depth < max_depth:
                        stack.append((path, depth + 1))
                    else:
                        skipped.append({"path": str(path), "reason": "max_depth"})
                    continue
                if not entry.is_file(follow_symlinks=False):
                    continue
            except OSError as exc:
                skipped.append({"path": str(path), "reason": "entry_unreadable", "detail": str(exc)})
                continue
            if not any(fnmatch.fnmatch(entry.name, pattern) for pattern in patterns):
                continue
            if yielded >= max_files:
                raise ScanStopped(f"Per-root file limit reached at {root}: {max_files}")
            yielded += 1
            yield path


def atomic_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def read_limited(path: Path, state: dict, limits: dict, skipped: list[dict]) -> bytes | None:
    try:
        size = path.stat().st_size
    except OSError as exc:
        skipped.append({"path": str(path), "reason": "stat_failed", "detail": str(exc)})
        return None
    if size > limits["max_bytes_per_file"]:
        skipped.append({"path": str(path), "reason": "max_bytes_per_file", "size": size})
        return None
    if state["files_read"] >= limits["max_total_files"]:
        raise ScanStopped(f"Global file limit reached: {limits['max_total_files']}")
    if state["bytes_read"] + size > limits["max_total_bytes"]:
        raise ScanStopped(f"Global byte limit reached: {limits['max_total_bytes']}")
    try:
        data = path.read_bytes()
    except OSError as exc:
        skipped.append({"path": str(path), "reason": "read_failed", "detail": str(exc)})
        return None
    state["files_read"] += 1
    state["bytes_read"] += len(data)
    return data


def frontmatter_name(text: str, fallback: str) -> str:
    match = re.search(r"(?m)^name:\s*([^\r\n]+?)\s*$", text[:8192])
    return match.group(1).strip().strip('"\'') if match else fallback


def normalized(value: str) -> str:
    value = value.casefold().replace("_", "-").replace(" ", "-")
    return re.sub(r"[^a-z0-9-]+", "", value).strip("-")


def catalogue_entry(path: Path, row: dict, data: bytes) -> dict:
    text = data.decode("utf-8-sig", errors="replace")
    if row["kind"] == "skill":
        fallback = path.parent.name
        name = frontmatter_name(text, fallback)
    else:
        name = path.stem
    return {
        "name": name,
        "slug": normalized(name),
        "kind": row["kind"],
        "classification": row.get("classification", "project"),
        "root_id": row["id"],
        "path": str(path),
        "size": len(data),
        "sha256": sha256_bytes(data),
    }


def repository_coverage(repository_root: Path, report: dict, state: dict, limits: dict) -> dict:
    packaged = {"skill": set(), "workflow": set()}
    vendored: set[str] = set()
    skipped = report["skipped"]
    named_roots = [
        (repository_root / "skills", "skill", ["SKILL.md"], 2),
        (repository_root / "workflows", "workflow", ["*.md"], 4),
    ]
    for root, kind, patterns, depth in named_roots:
        if not root.is_dir():
            continue
        for path in iter_bounded_files(
            root,
            patterns=patterns,
            max_depth=depth,
            excludes=DEFAULT_EXCLUDES,
            max_files=limits["max_files_per_root"],
            skipped=skipped,
        ):
            data = read_limited(path, state, limits, skipped)
            if data is None:
                continue
            name = frontmatter_name(data.decode("utf-8-sig", errors="replace"), path.parent.name) if kind == "skill" else path.stem
            packaged[kind].add(normalized(name))
    vendor_root = repository_root / "vendor" / "skill-dependencies"
    if vendor_root.is_dir():
        for path in iter_bounded_files(
            vendor_root,
            patterns=["SKILL.md"],
            max_depth=4,
            excludes=DEFAULT_EXCLUDES,
            max_files=limits["max_files_per_root"],
            skipped=skipped,
        ):
            data = read_limited(path, state, limits, skipped)
            if data is not None:
                vendored.add(normalized(frontmatter_name(data.decode("utf-8-sig", errors="replace"), path.parent.name)))
    route_targets: set[str] = set()
    manifests = sorted({*repository_root.glob("*-routes.json"), repository_root / "routes.json"})
    manifests = [path for path in manifests if path.is_file()]
    if len(manifests) > limits["max_route_manifests"]:
        raise ScanStopped(f"Route-manifest limit reached: {limits['max_route_manifests']}")
    for path in manifests:
        data = read_limited(path, state, limits, skipped)
        if data is None:
            continue
        try:
            rows = json.loads(data.decode("utf-8-sig"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            skipped.append({"path": str(path), "reason": "invalid_route_manifest", "detail": str(exc)})
            continue
        for row in rows if isinstance(rows, list) else []:
            target = str(row.get("target", ""))
            if target:
                route_targets.add(normalized(Path(target).parent.name if target.endswith("SKILL.md") else Path(target).stem))
    return {
        "packaged": {key: sorted(value) for key, value in packaged.items()},
        "vendored_dependencies": sorted(vendored),
        "route_targets": sorted(route_targets),
    }


def mention_tokens(entry: dict) -> set[str]:
    tokens = {entry["slug"], normalized(Path(entry["path"]).stem)}
    if entry["kind"] == "skill":
        tokens.add(normalized(Path(entry["path"]).parent.name))
    return {token for token in tokens if len(token) >= 4 and token != "skill"}


def match_mentions(text: str, catalogue: list[dict]) -> list[str]:
    haystack = normalized(text)
    matched = []
    for entry in catalogue:
        if any(token in haystack for token in mention_tokens(entry)):
            matched.append(entry["slug"])
    return sorted(set(matched))


def initial_report(manifest: dict, manifest_hash: str) -> dict:
    return {
        "schema": SCHEMA,
        "manifest_sha256": manifest_hash,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scan_complete": False,
        "truncated": False,
        "stopped_reason": None,
        "completed_phases": [],
        "catalogue": [],
        "usage_files": [],
        "coverage": {},
        "candidates": [],
        "skipped": [],
        "stats": {"files_read": 0, "bytes_read": 0},
    }


def run_scan(manifest_path: Path, output_path: Path, *, resume: bool = False) -> tuple[dict, int]:
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes.decode("utf-8-sig"))
    if manifest.get("schema") != SCHEMA:
        raise ValueError(f"Expected schema {SCHEMA}")
    manifest_hash = sha256_bytes(manifest_bytes)
    base = manifest_path.parent.resolve()
    workspace_root = canonical(manifest["workspace_root"], base)
    allowed_roots = [canonical(item, base) for item in manifest.get("allowed_roots", [str(workspace_root)])]
    repository_root = canonical(manifest["repository_root"], base)
    limits = {
        "max_total_files": 500,
        "max_files_per_root": 250,
        "max_bytes_per_file": 512 * 1024,
        "max_total_bytes": 32 * 1024 * 1024,
        "max_route_manifests": 100,
        **manifest.get("limits", {}),
    }
    for name, value in limits.items():
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"Limit must be a positive integer: {name}")
    report = initial_report(manifest, manifest_hash)
    if resume and output_path.exists():
        prior = json.loads(output_path.read_text(encoding="utf-8-sig"))
        if prior.get("manifest_sha256") != manifest_hash:
            raise ValueError("Cannot resume: manifest hash changed")
        report = prior
        report["generated_at_utc"] = datetime.now(timezone.utc).isoformat()
        report["stopped_reason"] = None
        report["truncated"] = False
    state = report["stats"]

    def checkpoint(phase: str) -> None:
        if phase not in report["completed_phases"]:
            report["completed_phases"].append(phase)
        report["generated_at_utc"] = datetime.now(timezone.utc).isoformat()
        atomic_json(output_path, report)

    try:
        for row in manifest.get("catalog_roots", []):
            phase = f"catalog:{row['id']}"
            if phase in report["completed_phases"]:
                continue
            root = canonical(row["path"], base)
            validate_scan_root(root, workspace_root=workspace_root, allowed_roots=allowed_roots)
            if not root.is_dir():
                report["skipped"].append({"path": str(root), "reason": "catalog_root_missing", "root_id": row["id"]})
                checkpoint(phase)
                continue
            patterns = row.get("patterns") or (["SKILL.md"] if row["kind"] == "skill" else ["*.md"])
            excludes = DEFAULT_EXCLUDES | set(row.get("exclude", []))
            for path in iter_bounded_files(
                root,
                patterns=patterns,
                max_depth=int(row.get("max_depth", 2)),
                excludes=excludes,
                max_files=int(row.get("max_files", limits["max_files_per_root"])),
                skipped=report["skipped"],
            ):
                data = read_limited(path, state, limits, report["skipped"])
                if data is not None:
                    report["catalogue"].append(catalogue_entry(path, row, data))
            checkpoint(phase)

        for row in manifest.get("usage_roots", []):
            phase = f"usage:{row['id']}"
            if phase in report["completed_phases"]:
                continue
            root = canonical(row["path"], base)
            validate_scan_root(root, workspace_root=workspace_root, allowed_roots=allowed_roots)
            if not root.is_dir():
                report["skipped"].append({"path": str(root), "reason": "usage_root_missing", "root_id": row["id"]})
                checkpoint(phase)
                continue
            for path in iter_bounded_files(
                root,
                patterns=row.get("patterns", ["*.md", "*.json"]),
                max_depth=int(row.get("max_depth", 1)),
                excludes=DEFAULT_EXCLUDES | set(row.get("exclude", [])),
                max_files=int(row.get("max_files", limits["max_files_per_root"])),
                skipped=report["skipped"],
            ):
                data = read_limited(path, state, limits, report["skipped"])
                if data is None:
                    continue
                text = data.decode("utf-8-sig", errors="replace")
                slugs = match_mentions(text, report["catalogue"])
                report["usage_files"].append({"path": str(path), "root_id": row["id"], "mentions": slugs})
            checkpoint(phase)

        phase = "usage:explicit-files"
        if phase not in report["completed_phases"]:
            for raw in manifest.get("usage_files", []):
                path = canonical(raw, base)
                if not is_within(path, allowed_roots):
                    raise ValueError(f"Usage file is outside allowed_roots: {path}")
                if not path.is_file() or is_link_or_junction(path):
                    report["skipped"].append({"path": str(path), "reason": "usage_file_missing_or_link"})
                    continue
                data = read_limited(path, state, limits, report["skipped"])
                if data is not None:
                    text = data.decode("utf-8-sig", errors="replace")
                    report["usage_files"].append({"path": str(path), "root_id": "explicit-files", "mentions": match_mentions(text, report["catalogue"])})
            checkpoint(phase)

        phase = "coverage"
        if phase not in report["completed_phases"]:
            validate_scan_root(repository_root, workspace_root=workspace_root, allowed_roots=allowed_roots)
            report["coverage"] = repository_coverage(repository_root, report, state, limits)
            counts: dict[str, int] = {}
            evidence: dict[str, list[str]] = {}
            for usage in report["usage_files"]:
                for slug in usage["mentions"]:
                    counts[slug] = counts.get(slug, 0) + 1
                    evidence.setdefault(slug, [])
                    if len(evidence[slug]) < 10:
                        evidence[slug].append(usage["path"])
            packaged = {kind: set(values) for kind, values in report["coverage"]["packaged"].items()}
            vendored = set(report["coverage"].get("vendored_dependencies", []))
            routed = set(report["coverage"]["route_targets"])
            for entry in report["catalogue"]:
                slug = entry["slug"]
                observed = counts.get(slug, 0)
                if slug in vendored:
                    status = "vendored_dependency"
                elif entry["classification"] in {"external", "system", "vendor"}:
                    status = "external_dependency"
                elif slug in packaged.get(entry["kind"], set()) or slug in routed:
                    status = "already_packaged"
                elif observed:
                    status = "used_missing"
                else:
                    status = "not_observed"
                report["candidates"].append({
                    "name": entry["name"],
                    "slug": slug,
                    "kind": entry["kind"],
                    "root_id": entry["root_id"],
                    "source_path": entry["path"],
                    "classification": entry["classification"],
                    "status": status,
                    "usage_file_count": observed,
                    "usage_evidence": evidence.get(slug, []),
                    "action": "review_for_reusable_packaging" if status == "used_missing" else "retain_reference_or_resolve_licence" if status == "external_dependency" else "none",
                })
            report["candidates"].sort(key=lambda item: (item["status"], item["kind"], item["slug"], item["source_path"]))
            checkpoint(phase)
        report["scan_complete"] = True
        atomic_json(output_path, report)
        return report, 0
    except ScanStopped as exc:
        report["truncated"] = True
        report["stopped_reason"] = str(exc)
        report["scan_complete"] = False
        atomic_json(output_path, report)
        return report, 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--resume", action="store_true", help="Resume only root phases from an output with the same manifest hash")
    options = parser.parse_args(argv)
    try:
        report, code = run_scan(options.manifest.resolve(), options.output.resolve(), resume=options.resume)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"schema": SCHEMA, "error": str(exc)}), file=sys.stderr)
        return 1
    print(json.dumps({
        "scan_complete": report["scan_complete"],
        "truncated": report["truncated"],
        "catalogue_entries": len(report["catalogue"]),
        "usage_files": len(report["usage_files"]),
        "used_missing": sum(item["status"] == "used_missing" for item in report["candidates"]),
        "files_read": report["stats"]["files_read"],
        "bytes_read": report["stats"]["bytes_read"],
    }))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
