import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("installer", ROOT / "install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class FrameRudimentsRoutes(unittest.TestCase):
    def test_real_route_set_preserves_unrelated_text_and_is_idempotent(self):
        routes = json.loads((ROOT / "framerudiments-routes.json").read_text())
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            originals = {}
            for row in routes:
                if row["mode"] == "insert":
                    path = target / row["target"]
                    path.parent.mkdir(parents=True, exist_ok=True)
                    text = "Private retained prefix\n\n" + row["anchor"] + "\nPrivate retained suffix\n"
                    path.write_text(text, encoding="utf-8")
                    originals[row["target"]] = text
            installer.install(target, ROOT, manifest="framerudiments-routes.json")
            for row in routes:
                if row["mode"] == "insert":
                    text = (target / row["target"]).read_text(encoding="utf-8")
                    snippet = (ROOT / row["source"]).read_text(encoding="utf-8").strip()
                    self.assertEqual(text.replace(snippet + "\n\n", "", 1), originals[row["target"]])
            self.assertTrue(all(x["status"] == "current" for x in installer.install(
                target, ROOT, check=True, manifest="framerudiments-routes.json")))
