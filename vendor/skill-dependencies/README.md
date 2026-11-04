# Vendored skill dependencies

This directory retains exact redistributable dependency snapshots used by WorkflowMoves. It is not the active Codex system-skill directory and installation routes never overwrite provider-managed `.system` or plugin locations.

The four `codex-system/` snapshots include each skill's `SKILL.md`, references, scripts, assets, agent metadata and Apache-2.0 licence exactly as observed on 27 October 2026. `external-skill-dependencies.json` records file counts, byte totals and deterministic tree hashes; `tools/audit_vendored_skill_dependencies.py` verifies them.

The Browser plugin is inventoried but not copied because its provider manifest declares `Proprietary`. Its version and hashes are retained so an installed copy can be resolved and compared without redistributing the body. The unlisted `review-agent` snapshot is likewise not copied because no redistribution licence was present.

Vendored source is evidence of a dependency snapshot, not proof that the runtime loaded it or that its instructions remain current. At use time, prefer the provider's currently installed skill when available and compare identity/version before relying on a vendored fallback.
