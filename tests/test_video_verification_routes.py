import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("video_qa_installer", ROOT / "install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)

class VideoVerificationRoutes(unittest.TestCase):
    def setUp(self):
        self.routes = json.loads((ROOT / "video-verification-routes.json").read_text(encoding="utf-8"))

    def fixture(self, workspace):
        originals = {}
        for row in self.routes:
            if row["mode"] == "insert":
                target = workspace / row["target"]
                target.parent.mkdir(parents=True, exist_ok=True)
                original = ("\ufeffPrivate ownership and quality contract.\r\n\r\n" + row["anchor"] + "\r\nPreserve approval and dates.\r\n").encode("utf-8")
                target.write_bytes(original)
                originals[row["target"]] = original
        return originals

    def test_preview_is_read_only_and_install_preserves_original_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            originals = self.fixture(workspace)
            preview = installer.install(workspace, ROOT, check=True, manifest="video-verification-routes.json")
            self.assertEqual(len(preview), 8)
            self.assertTrue(all(row["status"] == "pending" for row in preview))
            self.assertFalse((workspace / self.routes[0]["target"]).exists())
            for rel, original in originals.items():
                self.assertEqual((workspace / rel).read_bytes(), original)
            installer.install(workspace, ROOT, manifest="video-verification-routes.json")
            block = (ROOT / "fragments/rendered-video-verification.md").read_text(encoding="utf-8").strip().replace("\n", "\r\n").encode("utf-8") + b"\r\n\r\n"
            for rel, original in originals.items():
                actual = (workspace / rel).read_bytes()
                self.assertEqual(actual.count(block), 1)
                self.assertEqual(actual.replace(block, b"", 1), original)
            for row in self.routes:
                if row["mode"] == "copy":
                    self.assertEqual((workspace / row["target"]).read_bytes(), (ROOT / row["source"]).read_bytes())
            repeat = installer.install(workspace, ROOT, check=True, manifest="video-verification-routes.json")
            self.assertTrue(all(row["status"] == "current" for row in repeat))

    def test_late_conflict_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            originals = self.fixture(workspace)
            last = self.routes[-1]
            (workspace / last["target"]).write_bytes(b"Project-owned guide without an anchor.\n")
            with self.assertRaises(ValueError):
                installer.install(workspace, ROOT, manifest="video-verification-routes.json")
            self.assertFalse((workspace / self.routes[0]["target"]).exists())
            for rel, original in originals.items():
                if rel != last["target"]:
                    self.assertEqual((workspace / rel).read_bytes(), original)

    def test_modified_installed_skill_is_preserved_as_conflict(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self.fixture(workspace)
            installer.install(workspace, ROOT, manifest="video-verification-routes.json")
            target = workspace / ".agents/skills/verify-rendered-music-video/SKILL.md"
            changed = target.read_bytes() + b"\nProject-specific review gate.\n"
            target.write_bytes(changed)
            with self.assertRaises(ValueError):
                installer.install(workspace, ROOT, manifest="video-verification-routes.json")
            self.assertEqual(target.read_bytes(), changed)

    def test_illustration_link_resolves_and_skill_has_focused_identity(self):
        guide = (ROOT / "workflows/rendered-video-verification.md").read_text(encoding="utf-8")
        self.assertIn("media/rendered-video-verification.svg", guide)
        self.assertTrue((ROOT / "workflows/media/rendered-video-verification.svg").is_file())
        skill = (ROOT / "skills/verify-rendered-music-video/SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\nname: verify-rendered-music-video\n"))
        self.assertIn("attended-listening", skill)

if __name__ == "__main__":
    unittest.main()
