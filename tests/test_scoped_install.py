import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('scoped_install', Path(__file__).resolve().parents[1] / 'install.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ScopedInstall(unittest.TestCase):
    def test_selected_routes_preserve_unrelated_conflicting_owner_and_repeat(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'workspace'; package = Path(temp) / 'package'
            root.mkdir(); package.mkdir()
            (root / 'selected.md').write_bytes(b'\xef\xbb\xbf# Keep\r\n\r\n## Anchor\r\nTail\r\n')
            private = b'## Managed\nAnother owner changed this\n'
            (root / 'other.md').write_bytes(private)
            (package / 'fragment.md').write_text('## Managed\nNew\n')
            row = dict(target='selected.md', source='fragment.md', mode='insert', anchor='## Anchor', identity='## Managed')
            (package / 'selected.json').write_text(json.dumps([row]))
            (package / 'routes.json').write_text(json.dumps([row, dict(row, target='other.md')]))
            with self.assertRaises(ValueError):
                mod.install(root, package)
            self.assertNotIn(b'## Managed', (root / 'selected.md').read_bytes())
            result = mod.install(root, package, manifest='selected.json')
            self.assertEqual(len(result), 1)
            self.assertEqual((root / 'selected.md').read_bytes(), b'\xef\xbb\xbf# Keep\r\n\r\n## Managed\r\nNew\r\n\r\n## Anchor\r\nTail\r\n')
            self.assertEqual((root / 'other.md').read_bytes(), private)
            self.assertEqual(mod.install(root, package, manifest='selected.json')[0]['status'], 'current')

    def test_route_manifest_cannot_leave_package(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'workspace'; package = Path(temp) / 'package'
            root.mkdir(); package.mkdir()
            (Path(temp) / 'outside.json').write_text('[]')
            with self.assertRaisesRegex(ValueError, 'Path leaves workspace'):
                mod.install(root, package, manifest='../outside.json')
