"""Focused integration upgrades must preserve surrounding project instructions."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

PACKAGE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('focused_installer', PACKAGE/'install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class PreviewIntegrationRoutes(unittest.TestCase):
    def test_preview_apply_and_repeat_preserve_unrelated_text(self):
        for manifest in ('potbot-unity-routes.json', 'potbot-unity-guidance-routes.json', 'tool-learning-routes.json'):
            with self.subTest(manifest=manifest), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                routes = json.loads((PACKAGE/manifest).read_text('utf-8'))
                before = {}
                for route in routes:
                    target = root/route['target']
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if route['mode'] == 'insert':
                        target.write_text('Unrelated project-owned text.\n\n'+route['anchor']+'\n\nRetained tail.\n', encoding='utf-8')
                    elif route.get('previous_source'):
                        target.write_bytes((PACKAGE/route['previous_source']).read_bytes())
                    before[route['target']] = target.read_bytes() if target.exists() else None
                installer.install(root, check=True, manifest=manifest)
                for relative, data in before.items():
                    target = root/relative
                    self.assertEqual(target.read_bytes() if target.exists() else None, data)
                installer.install(root, manifest=manifest)
                installed = {route['target']:(root/route['target']).read_bytes() for route in routes}
                installer.install(root, manifest=manifest)
                self.assertEqual(installed, {relative:(root/relative).read_bytes() for relative in installed})
                for route in routes:
                    if route['mode']=='insert':
                        text=(root/route['target']).read_text('utf-8')
                        self.assertTrue(text.startswith('Unrelated project-owned text.'))
                        self.assertTrue(text.endswith('Retained tail.\n'))

if __name__=='__main__':
    unittest.main()
