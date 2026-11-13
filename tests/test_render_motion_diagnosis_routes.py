import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "render-motion-diagnosis-routes.json"
spec = importlib.util.spec_from_file_location("render_motion_installer", ROOT / "install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class RenderMotionRoutes(unittest.TestCase):
    def test_install_preserves_rendering_instructions_and_copies_exact_demo(self):
        rows = json.loads((ROOT / MANIFEST).read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            originals = {}
            for row in rows:
                if row["mode"] == "insert":
                    target = workspace / row["target"]
                    target.parent.mkdir(parents=True, exist_ok=True)
                    original = (
                        "\ufeffProject timing rules\r\n\r\n## Verify the exact encoded film"
                        f"\r\nKeep this verification block.\r\n\r\n{row['anchor']}\r\n"
                    ).encode("utf-8")
                    target.write_bytes(original)
                    originals[row["target"]] = original

            preview = installer.install(workspace, ROOT, check=True, manifest=MANIFEST)
            self.assertTrue(all(row["status"] == "pending" for row in preview))
            for relative, original in originals.items():
                self.assertEqual((workspace / relative).read_bytes(), original)

            installer.install(workspace, ROOT, manifest=MANIFEST)
            for row in rows:
                actual = (workspace / row["target"]).read_bytes()
                source = (ROOT / row["source"]).read_bytes()
                if row["mode"] == "copy":
                    self.assertEqual(actual, source)
                else:
                    added = source.strip().replace(b"\n", b"\r\n") + b"\r\n\r\n"
                    self.assertEqual(actual.count(added), 1)
                    self.assertEqual(actual.replace(added, b""), originals[row["target"]])

            media = workspace / "Workflows/media"
            receipt = json.loads((media / "render-motion-comparison.json").read_text(encoding="utf-8"))
            self.assertEqual(
                hashlib.sha256((media / "render-motion-comparison.mp4").read_bytes()).hexdigest(),
                receipt["video_sha256"],
            )
            repeated = installer.install(workspace, ROOT, check=True, manifest=MANIFEST)
            self.assertTrue(all(row["status"] == "current" for row in repeated))
