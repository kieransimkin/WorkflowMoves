import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("discovery_installer", ROOT / "install.py")
INSTALLER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSTALLER)


class SkillWorkflowDiscoveryRoutesTests(unittest.TestCase):
    def setUp(self):
        self.routes = json.loads((ROOT / "skill-workflow-discovery-routes.json").read_text(encoding="utf-8"))

    def test_preview_install_and_repeat_are_guarded(self):
        with tempfile.TemporaryDirectory() as folder:
            workspace = Path(folder)
            preview = INSTALLER.install(workspace, ROOT, check=True, manifest="skill-workflow-discovery-routes.json")
            self.assertEqual(len(preview), 6)
            self.assertTrue(all(row["status"] == "pending" for row in preview))
            self.assertFalse((workspace / "Tools/discover_skill_workflow_usage.py").exists())
            INSTALLER.install(workspace, ROOT, manifest="skill-workflow-discovery-routes.json")
            for row in self.routes:
                self.assertEqual((workspace / row["target"]).read_bytes(), (ROOT / row["source"]).read_bytes())
            repeat = INSTALLER.install(workspace, ROOT, check=True, manifest="skill-workflow-discovery-routes.json")
            self.assertTrue(all(row["status"] == "current" for row in repeat))

    def test_modified_destination_stops_all_writes(self):
        with tempfile.TemporaryDirectory() as folder:
            workspace = Path(folder)
            INSTALLER.install(workspace, ROOT, manifest="skill-workflow-discovery-routes.json")
            target = workspace / "Workflows/skill-workflow-discovery.md"
            changed = target.read_bytes() + b"\nProject-owned addition.\n"
            target.write_bytes(changed)
            with self.assertRaises(ValueError):
                INSTALLER.install(workspace, ROOT, manifest="skill-workflow-discovery-routes.json")
            self.assertEqual(target.read_bytes(), changed)

    def test_docs_media_and_external_dependency_register_exist(self):
        workflow = (ROOT / "workflows/skill-workflow-discovery.md").read_text(encoding="utf-8")
        self.assertIn("media/skill-workflow-discovery.svg", workflow)
        self.assertTrue((ROOT / "workflows/media/skill-workflow-discovery.svg").is_file())
        dependencies = json.loads((ROOT / "external-skill-dependencies.json").read_text(encoding="utf-8"))
        identities = {row["id"] for row in dependencies["dependencies"]}
        self.assertIn("browser:control-in-app-browser", identities)
        self.assertIn("skill-creator", identities)


if __name__ == "__main__":
    unittest.main()
