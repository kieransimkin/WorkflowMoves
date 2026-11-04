import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("identified_installer", ROOT / "install.py")
INSTALLER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSTALLER)


class IdentifiedWorkflowRoutesTests(unittest.TestCase):
    def setUp(self):
        self.routes = json.loads((ROOT / "identified-workflows-routes.json").read_text(encoding="utf-8"))

    def test_fresh_install_is_exact_and_repeatable(self):
        with tempfile.TemporaryDirectory() as folder:
            workspace = Path(folder)
            preview = INSTALLER.install(workspace, ROOT, check=True, manifest="identified-workflows-routes.json")
            self.assertEqual(len(preview), 5)
            self.assertTrue(all(row["status"] == "pending" for row in preview))
            INSTALLER.install(workspace, ROOT, manifest="identified-workflows-routes.json")
            for row in self.routes:
                self.assertEqual((workspace / row["target"]).read_bytes(), (ROOT / row["source"]).read_bytes())
            self.assertTrue(all(row["status"] == "current" for row in INSTALLER.install(workspace, ROOT, check=True, manifest="identified-workflows-routes.json")))

    def test_existing_different_project_workflow_is_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            workspace = Path(folder)
            target = workspace / self.routes[0]["target"]
            target.parent.mkdir(parents=True)
            original = b"# Project-owned recovery\n\nHistorical private evidence.\n"
            target.write_bytes(original)
            with self.assertRaises(ValueError):
                INSTALLER.install(workspace, ROOT, manifest="identified-workflows-routes.json")
            self.assertEqual(target.read_bytes(), original)
            self.assertFalse((workspace / self.routes[1]["target"]).exists())

    def test_media_resolves_and_machine_specific_executable_is_not_frozen(self):
        patch_workflow = (ROOT / "workflows/campaign-safe-editor-recovery.md").read_text(encoding="utf-8")
        likeness = (ROOT / "workflows/likenessforge-image-preparation.md").read_text(encoding="utf-8")
        self.assertIn("media/campaign-safe-editor-recovery.svg", patch_workflow)
        self.assertIn("media/likenessforge-model-storage.svg", likeness)
        self.assertNotIn("C:\\Users\\Kieran", patch_workflow)
        self.assertTrue((ROOT / "vendor/likenessforge-media/LICENSE").is_file())


if __name__ == "__main__":
    unittest.main()
