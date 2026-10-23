import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("hashtag_installer", ROOT / "install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class HashtagRoutes(unittest.TestCase):
    def test_scoped_install_preserves_original_bytes_and_is_idempotent(self):
        routes = json.loads((ROOT / "hashtag-routes.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as d:
            workspace = Path(d)
            originals = {}
            for row in routes:
                if row["mode"] == "insert":
                    path = workspace / row["target"]
                    path.parent.mkdir(parents=True, exist_ok=True)
                    original = ("Private existing introduction\r\n\r\n" + row["anchor"] + "\r\nOriginal stop and approval rules.\r\n").encode("utf-8")
                    path.write_bytes(original)
                    originals[row["target"]] = original
            preview = installer.install(workspace, ROOT, check=True, manifest="hashtag-routes.json")
            self.assertEqual(len(preview), 17)
            for rel, data in originals.items():
                self.assertEqual((workspace / rel).read_bytes(), data)
            installer.install(workspace, ROOT, manifest="hashtag-routes.json")
            block = (ROOT / "fragments/hashtag-discovery-and-use.md").read_text(encoding="utf-8").strip().replace("\n", "\r\n").encode("utf-8") + b"\r\n\r\n"
            for rel, data in originals.items():
                self.assertEqual((workspace / rel).read_bytes().replace(block, b"", 1), data)
            again = installer.install(workspace, ROOT, check=True, manifest="hashtag-routes.json")
            self.assertTrue(all(x["status"] == "current" for x in again))

    def test_feature_contract_keeps_counts_and_authority_separate(self):
        text = (ROOT / "workflows/hashtag-discovery-and-use.md").read_text(encoding="utf-8")
        for token in ["editorial", "21-column", "metadata.passed", "Whole-post", "Blogworthiness", "Threads", "Pinterest", "Spotify", "no-op"]:
            self.assertIn(token, text)
        routes = json.loads((ROOT / "hashtag-routes.json").read_text(encoding="utf-8"))
        self.assertFalse(any("automations/" in x["target"] for x in routes))


if __name__ == "__main__":
    unittest.main()
