import json
from pathlib import Path
import tempfile
import unittest

import install


PACKAGE = Path(__file__).resolve().parents[1]
MANIFEST = "framerudiments-feature-routes.json"


class FrameRudimentsFeatureRoutes(unittest.TestCase):
    def test_feature_route_preserves_local_text_and_is_idempotent(self):
        routes = json.loads((PACKAGE / MANIFEST).read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            originals = {}
            for route in routes:
                if route["mode"] != "insert":
                    continue
                path = workspace / route["target"]
                path.parent.mkdir(parents=True, exist_ok=True)
                original = (
                    "\ufeffPrivate renderer, clock and output requirements.\r\n\r\n"
                    + route["anchor"]
                    + "\r\nRetain local preset and approval policy.\r\n"
                ).encode("utf-8")
                path.write_bytes(original)
                originals[path] = original
            guide = workspace / routes[0]["target"]
            preview = install.install(workspace, PACKAGE, check=True, manifest=MANIFEST)
            self.assertTrue(all(row["status"] == "pending" for row in preview))
            self.assertFalse(guide.exists())
            for path, original in originals.items():
                self.assertEqual(path.read_bytes(), original)
            install.install(workspace, PACKAGE, manifest=MANIFEST)
            self.assertEqual(guide.read_bytes(), (PACKAGE / routes[0]["source"]).read_bytes())
            for route in routes:
                if route["mode"] != "insert":
                    continue
                path = workspace / route["target"]
                block = (PACKAGE / route["source"]).read_text(encoding="utf-8").strip()
                added = (block.replace("\n", "\r\n") + "\r\n\r\n").encode("utf-8")
                self.assertEqual(path.read_bytes().count(added), 1)
                self.assertEqual(path.read_bytes().replace(added, b"", 1), originals[path])
            current = install.install(workspace, PACKAGE, check=True, manifest=MANIFEST)
            self.assertTrue(all(row["status"] == "current" for row in current))
            baseline = PACKAGE / routes[0]["previous_source"]
            guide.write_bytes(baseline.read_bytes())
            upgraded = install.install(workspace, PACKAGE, manifest=MANIFEST)
            changed = [Path(row["target"]) for row in upgraded if row["status"] == "updated"]
            self.assertEqual(changed, [guide.resolve()])
            self.assertEqual(guide.read_bytes(), (PACKAGE / routes[0]["source"]).read_bytes())


if __name__ == "__main__":
    unittest.main()
