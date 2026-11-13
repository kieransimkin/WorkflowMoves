import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


PACKAGE = Path(__file__).resolve().parents[1]
MANIFEST = "stemlab-word-timing-routes.json"
spec = importlib.util.spec_from_file_location("word_timing_installer", PACKAGE / "install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


def windows_block(path):
    return path.read_text(encoding="utf-8-sig").strip().replace("\n", "\r\n").encode()


class StemLabWordTimingRoutes(unittest.TestCase):
    def test_upgrade_keeps_project_text_and_rejects_changed_predecessor(self):
        routes = json.loads((PACKAGE / MANIFEST).read_text(encoding="utf-8"))
        prefix = b"\xef\xbb\xbf# Local timing policy\r\n\r\n"
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            originals = {}
            expected = {}
            for row in routes:
                target = workspace / row["target"]
                target.parent.mkdir(parents=True, exist_ok=True)
                source = PACKAGE / row["source"]
                previous = PACKAGE / row["previous_source"] if "previous_source" in row else None
                if row["mode"] == "copy":
                    before = previous.read_bytes()
                    after = source.read_bytes()
                else:
                    suffix = row["anchor"].encode() + b"\r\nKeep this.\r\n"
                    before = prefix + (windows_block(previous) + b"\r\n\r\n" if previous else b"") + suffix
                    after = prefix + windows_block(source) + b"\r\n\r\n" + suffix
                target.write_bytes(before)
                originals[target] = before
                expected[target] = after

            preview = installer.install(workspace, PACKAGE, check=True, manifest=MANIFEST)
            self.assertTrue(all(row["status"] == "pending" for row in preview))
            self.assertEqual({path: path.read_bytes() for path in originals}, originals)

            modified = workspace / "Workflows/stemlab-lyric-timing-audition.md"
            modified.write_bytes(originals[modified].replace(b"ranked whole-song scores", b"reviewed manually"))
            self.assertNotEqual(modified.read_bytes(), originals[modified])
            with self.assertRaisesRegex(ValueError, "Existing managed block differs"):
                installer.install(workspace, PACKAGE, manifest=MANIFEST)
            self.assertEqual({path: path.read_bytes() for path in originals if path != modified},
                             {path: content for path, content in originals.items() if path != modified})

            modified.write_bytes(originals[modified])
            installer.install(workspace, PACKAGE, manifest=MANIFEST)
            self.assertEqual({path: path.read_bytes() for path in expected}, expected)
            repeat = installer.install(workspace, PACKAGE, check=True, manifest=MANIFEST)
            self.assertTrue(all(row["status"] == "current" for row in repeat))
