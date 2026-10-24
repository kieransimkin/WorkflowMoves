import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("cyclic_event_installer", ROOT / "install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class CyclicEventRoutes(unittest.TestCase):
    def setUp(self):
        self.routes = json.loads((ROOT / "cyclic-event-routes.json").read_text(encoding="utf-8"))

    def fixture(self, workspace):
        originals = {}
        for row in self.routes:
            if row["mode"] == "insert":
                target = workspace / row["target"]
                target.parent.mkdir(parents=True, exist_ok=True)
                original = ("\ufeffExisting instructions and private ownership.\r\n\r\n" + row["anchor"] + "\r\nPreserve the exact approved scope and dates outside it.\r\n").encode("utf-8")
                target.write_bytes(original)
                originals[row["target"]] = original
        return originals

    def test_complete_install_preserves_bom_crlf_and_is_current_on_repeat(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            originals = self.fixture(workspace)
            preview = installer.install(workspace, ROOT, check=True, manifest="cyclic-event-routes.json")
            self.assertEqual(len(preview), 7)
            self.assertTrue(all(row["status"] == "pending" for row in preview))
            for rel, original in originals.items():
                self.assertEqual((workspace / rel).read_bytes(), original)
            self.assertFalse((workspace / "Workflows/cyclic-event-keyword-planning.md").exists())
            installer.install(workspace, ROOT, manifest="cyclic-event-routes.json")
            block = (ROOT / "fragments/cyclic-event-keyword-planning.md").read_text(encoding="utf-8").strip().replace("\n", "\r\n").encode("utf-8") + b"\r\n\r\n"
            for rel, original in originals.items():
                actual = (workspace / rel).read_bytes()
                self.assertEqual(actual.count(block), 1)
                self.assertEqual(actual.replace(block, b"", 1), original)
            for row in self.routes:
                if row["mode"] == "copy":
                    self.assertEqual((workspace / row["target"]).read_bytes(), (ROOT / row["source"]).read_bytes())
            repeated = installer.install(workspace, ROOT, check=True, manifest="cyclic-event-routes.json")
            self.assertTrue(all(row["status"] == "current" for row in repeated))

    def test_late_missing_anchor_causes_no_earlier_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            originals = self.fixture(workspace)
            last = self.routes[-1]
            target = workspace / last["target"]
            edited = b"Different project-owned guide, no known anchor.\n"
            target.write_bytes(edited)
            with self.assertRaisesRegex(ValueError, "Missing or ambiguous anchor"):
                installer.install(workspace, ROOT, manifest="cyclic-event-routes.json")
            self.assertFalse((workspace / self.routes[0]["target"]).exists())
            for rel, original in originals.items():
                self.assertEqual((workspace / rel).read_bytes(), edited if rel == last["target"] else original)

    def test_edited_managed_scope_is_a_conflict_not_a_silent_approval_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self.fixture(workspace)
            installer.install(workspace, ROOT, manifest="cyclic-event-routes.json")
            row = next(row for row in self.routes if row["mode"] == "insert")
            target = workspace / row["target"]
            edited = target.read_bytes().replace(b"evidence-backed rescheduling is allowed", b"project-specific reviewed wording", 1)
            target.write_bytes(edited)
            with self.assertRaisesRegex(ValueError, "Existing managed block differs"):
                installer.install(workspace, ROOT, manifest="cyclic-event-routes.json")
            self.assertEqual(target.read_bytes(), edited)

    def test_changed_copied_guide_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self.fixture(workspace)
            target = workspace / self.routes[0]["target"]
            target.write_bytes(b"Project-owned cyclic guide with a separate rule.\n")
            with self.assertRaisesRegex(ValueError, "Existing destination differs"):
                installer.install(workspace, ROOT, manifest="cyclic-event-routes.json")
            self.assertEqual(target.read_bytes(), b"Project-owned cyclic guide with a separate rule.\n")


if __name__ == "__main__":
    unittest.main()
