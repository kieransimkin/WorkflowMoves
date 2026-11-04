import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "skill_workflow_discovery", ROOT / "tools" / "discover_skill_workflow_usage.py"
)
DISCOVERY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DISCOVERY)


class SkillWorkflowDiscoveryTests(unittest.TestCase):
    def write_skill(self, root: Path, name: str) -> Path:
        path = root / name / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\nname: {name}\ndescription: Test skill.\n---\n\n# {name}\n", encoding="utf-8")
        return path

    def manifest(self, workspace: Path, repository: Path) -> dict:
        return {
            "schema": DISCOVERY.SCHEMA,
            "workspace_root": str(workspace),
            "allowed_roots": [str(workspace)],
            "repository_root": str(repository),
            "limits": {
                "max_total_files": 100,
                "max_files_per_root": 30,
                "max_bytes_per_file": 65536,
                "max_total_bytes": 1048576,
                "max_route_manifests": 20,
            },
            "catalog_roots": [
                {
                    "id": "project-skills",
                    "path": str(workspace / ".agents" / "skills"),
                    "kind": "skill",
                    "classification": "project",
                    "patterns": ["SKILL.md"],
                    "max_depth": 2,
                },
                {
                    "id": "external-skills",
                    "path": str(workspace / "provider" / "skills"),
                    "kind": "skill",
                    "classification": "external",
                    "patterns": ["SKILL.md"],
                    "max_depth": 2,
                },
                {
                    "id": "project-workflows",
                    "path": str(workspace / "Workflows"),
                    "kind": "workflow",
                    "classification": "project",
                    "patterns": ["*.md"],
                    "max_depth": 1,
                },
            ],
            "usage_roots": [
                {
                    "id": "coordination",
                    "path": str(workspace / ".codex" / "coordination"),
                    "patterns": ["*.md"],
                    "max_depth": 1,
                    "max_files": 10,
                }
            ],
            "usage_files": [],
        }

    def fixture(self, base: Path) -> tuple[Path, Path, Path]:
        workspace = base / "workspace"
        repository = workspace / "repo"
        repository.mkdir(parents=True)
        self.write_skill(repository / "skills", "covered-skill")
        (repository / "workflows").mkdir()
        (repository / "workflows" / "covered-flow.md").write_text("# Covered\n", encoding="utf-8")
        (repository / "sample-routes.json").write_text(
            json.dumps([{"target": "Workflows/routed-flow.md", "source": "x", "mode": "copy"}]),
            encoding="utf-8",
        )
        self.write_skill(workspace / ".agents" / "skills", "used-missing-skill")
        self.write_skill(workspace / ".agents" / "skills", "covered-skill")
        self.write_skill(workspace / "provider" / "skills", "browser-control-in-app-browser")
        workflows = workspace / "Workflows"
        workflows.mkdir()
        (workflows / "routed-flow.md").write_text("# Routed\n", encoding="utf-8")
        (workflows / "unused-flow.md").write_text("# Unused\n", encoding="utf-8")
        coordination = workspace / ".codex" / "coordination"
        coordination.mkdir(parents=True)
        (coordination / "task.md").write_text(
            "Used used-missing-skill and browser-control-in-app-browser, then followed routed-flow from Workflows.\n",
            encoding="utf-8",
        )
        manifest_path = workspace / "scan.json"
        manifest_path.write_text(json.dumps(self.manifest(workspace, repository)), encoding="utf-8")
        return workspace, repository, manifest_path

    def test_bounded_scan_classifies_packaged_missing_and_external(self):
        with tempfile.TemporaryDirectory() as folder:
            workspace, _, manifest_path = self.fixture(Path(folder))
            output = workspace / "result.json"
            report, code = DISCOVERY.run_scan(manifest_path, output)
            self.assertEqual(code, 0)
            self.assertTrue(report["scan_complete"])
            states = {(row["slug"], row["source_path"]): row["status"] for row in report["candidates"]}
            self.assertIn("used_missing", [status for (slug, _), status in states.items() if slug == "used-missing-skill"])
            self.assertIn("already_packaged", [status for (slug, _), status in states.items() if slug == "covered-skill"])
            self.assertIn("already_packaged", [status for (slug, _), status in states.items() if slug == "routed-flow"])
            self.assertIn("external_dependency", [status for (slug, _), status in states.items() if slug == "browser-control-in-app-browser"])
            self.assertIn("not_observed", [status for (slug, _), status in states.items() if slug == "unused-flow"])
            self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["manifest_sha256"], report["manifest_sha256"])

    def test_workspace_root_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            workspace, repository, _ = self.fixture(Path(folder))
            manifest = self.manifest(workspace, repository)
            manifest["catalog_roots"][0]["path"] = str(workspace)
            manifest_path = workspace / "bad.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Workspace-root traversal"):
                DISCOVERY.run_scan(manifest_path, workspace / "bad-result.json")

    def test_budget_stop_retains_partial_checkpoint(self):
        with tempfile.TemporaryDirectory() as folder:
            workspace, repository, _ = self.fixture(Path(folder))
            manifest = self.manifest(workspace, repository)
            manifest["limits"]["max_total_files"] = 1
            manifest_path = workspace / "small.json"
            output = workspace / "partial.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            report, code = DISCOVERY.run_scan(manifest_path, output)
            self.assertEqual(code, 2)
            self.assertTrue(report["truncated"])
            self.assertFalse(report["scan_complete"])
            retained = json.loads(output.read_text(encoding="utf-8"))
            self.assertIn("Global file limit", retained["stopped_reason"])

    def test_resume_requires_exact_manifest_hash(self):
        with tempfile.TemporaryDirectory() as folder:
            workspace, _, manifest_path = self.fixture(Path(folder))
            output = workspace / "result.json"
            DISCOVERY.run_scan(manifest_path, output)
            changed = json.loads(manifest_path.read_text(encoding="utf-8"))
            changed["limits"]["max_total_files"] += 1
            manifest_path.write_text(json.dumps(changed), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "manifest hash changed"):
                DISCOVERY.run_scan(manifest_path, output, resume=True)


if __name__ == "__main__":
    unittest.main()
