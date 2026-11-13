import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "video-production-review-routes.json"
spec = importlib.util.spec_from_file_location("video_production_installer", ROOT / "install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class VideoProductionReviewRoutes(unittest.TestCase):
    def test_install_preserves_project_guide_and_resolves_new_references(self):
        routes = json.loads((ROOT / MANIFEST).read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            originals = {}
            for row in routes:
                if row["mode"] == "insert":
                    target = workspace / row["target"]
                    target.parent.mkdir(parents=True, exist_ok=True)
                    original = f"\ufeffPrivate timing authority.\r\n{row['anchor']}\r\nKeep this.\r\n".encode("utf-8")
                    target.write_bytes(original)
                    originals[row["target"]] = original

            preview = installer.install(workspace, ROOT, check=True, manifest=MANIFEST)
            self.assertTrue(all(item["status"] == "pending" for item in preview))
            for rel, original in originals.items():
                self.assertEqual((workspace / rel).read_bytes(), original)
            installed = installer.install(workspace, ROOT, manifest=MANIFEST)
            self.assertEqual(
                [item["after_sha256"] for item in installed],
                [item["after_sha256"] for item in preview],
            )
            for row in routes:
                actual = (workspace / row["target"]).read_bytes()
                source = (ROOT / row["source"]).read_bytes()
                if row["mode"] == "copy":
                    self.assertEqual(actual, source)
                else:
                    block = source.strip().replace(b"\n", b"\r\n") + b"\r\n\r\n"
                    self.assertEqual(actual.count(block), 1)
                    self.assertEqual(actual.replace(block, b""), originals[row["target"]])
            for rel in ("media/video-revision-comparison.png", "media/video-revision-demo.mp4"):
                self.assertGreater((workspace / "Workflows" / rel).stat().st_size, 1000)
            repeat = installer.install(workspace, ROOT, check=True, manifest=MANIFEST)
            self.assertTrue(all(item["status"] == "current" for item in repeat))

    def test_upgrade_preserves_project_text_and_second_route(self):
        routes = json.loads((ROOT / MANIFEST).read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            originals = {}
            for row in routes:
                if row["mode"] != "insert":
                    continue
                target = workspace / row["target"]
                target.parent.mkdir(parents=True, exist_ok=True)
                previous = (ROOT / row["previous_source"]).read_text(encoding="utf-8").strip()
                before = "Project brief.\n\n"
                after = "\n\nProject verification guidance.\n\n" + row["anchor"] + "\n"
                originals[row["target"]] = (before, after)
                target.write_bytes((before + previous + after).encode("utf-8"))

            installer.install(workspace, ROOT, manifest=MANIFEST)
            for row in routes:
                if row["mode"] != "insert":
                    continue
                before, after = originals[row["target"]]
                current = (ROOT / row["source"]).read_text(encoding="utf-8").strip()
                actual = (workspace / row["target"]).read_bytes()
                self.assertEqual(actual, (before + current + after).encode("utf-8"))
