---
name: discover-skill-workflow-usage
description: Audit known skill/workflow locations and bounded project-chat evidence to find reusable items missing from WorkflowMoves. Use after project work reveals an untracked workflow or when replacing an unsafe broad scan; do not crawl a drive, infer use from installation alone, or copy external/system skills.
---

# Discover skill and workflow use safely

Follow the maintained [bounded discovery workflow](https://github.com/kieransimkin/WorkflowMoves/blob/main/workflows/skill-workflow-discovery.md), or the installed `Workflows/skill-workflow-discovery.md`.

1. Name every catalogue root and usage root in a private manifest. Prefer `.agents/skills/`, maintained `skill-source/`, `Workflows/`, `.codex/coordination/` and exact identified task reports. Never select a drive, workspace root or complete reports archive.
2. Classify bundled/system/vendor locations as external dependencies. Do not copy their instructions into the workflow repository.
3. Set conservative depth, file and byte budgets before running `Tools/discover_skill_workflow_usage.py`. Keep link/junction traversal disabled.
4. Require `scan_complete: true`. A partial checkpoint is recoverable evidence, not a complete inventory; reduce scope or use `--resume` with the unchanged manifest.
5. Review each `used_missing` candidate against its cited evidence and full source. Installation is not actual use, name matching is not semantic proof, and private/project-only instructions do not belong in the public package.
6. Package the smallest coherent public-safe skill/workflow, tests, route and useful documentation media. Preserve approval, rights, privacy and external-action gates.
7. Record packaged, already-covered, external, held or excluded for each reviewed candidate. Assess Blogworthiness separately and keep private scan paths/results out of Git.
