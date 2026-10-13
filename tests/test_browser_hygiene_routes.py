import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

PACKAGE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('hygiene_install', PACKAGE / 'install.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class BrowserHygieneRoutes(unittest.TestCase):
    def routes(self):
        return [row for row in json.loads((PACKAGE / 'routes.json').read_text(encoding='utf-8'))
                if 'browser-tab-hygiene' in row['source'] or 'browser-recovery-lessons' in row['source']]

    def fixture(self, root, package):
        rows = self.routes()
        self.assertEqual(len(rows), 5)
        for row in rows:
            source = package / row['source']
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_bytes((PACKAGE / row['source']).read_bytes())
            if row.get('previous_source'):
                prior_source = package / row['previous_source']
                prior_source.parent.mkdir(parents=True, exist_ok=True)
                prior_source.write_bytes((PACKAGE / row['previous_source']).read_bytes())
            if row['mode'] == 'insert':
                target = root / row['target']
                target.parent.mkdir(parents=True, exist_ok=True)
                if any(other['target'] == row['target'] and other.get('identity') == row['anchor'] for other in rows):
                    # This anchor is supplied by an earlier managed insertion.
                    continue
                prior = target.read_bytes() if target.exists() else b'\xef\xbb\xbf# Private prior material\r\n\r\n'
                target.write_bytes(prior + row['anchor'].encode() + b'\r\nKeep all old work\r\n')
        (package / 'routes.json').write_text(json.dumps(rows), encoding='utf-8')

    def test_hygiene_routes_preserve_existing_bytes_and_repeat(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'workspace'; package = Path(temp) / 'package'
            root.mkdir(); package.mkdir()
            self.fixture(root, package)
            planned = mod.plan(root, package)
            mod.install(root, package)
            for item in planned:
                after = Path(item['target']).read_bytes()
                self.assertEqual(after, item['after'])
                if item['before']:
                    # Removing exactly the additive block recovers all original bytes.
                    restored = after
                    for row in self.routes():
                        if (root / row['target']).resolve() == Path(item['target']):
                            snippet = (PACKAGE / row['source']).read_text(encoding='utf-8').strip().replace('\n', '\r\n')
                            restored = restored.replace((snippet + '\r\n\r\n').encode(), b'', 1)
                    self.assertEqual(restored, item['before'])
            self.assertTrue(all(r['status'] == 'current' for r in mod.install(root, package, check=True)))

    def test_modified_hygiene_rule_blocks_all_writes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'workspace'; package = Path(temp) / 'package'
            root.mkdir(); package.mkdir()
            self.fixture(root, package)
            target = root / 'AGENTS.md'
            target.write_text('## Close completed browser tabs\nConflicting rule\n\n## Form-field write verification\n', encoding='utf-8')
            before = {p: p.read_bytes() for p in root.rglob('*') if p.is_file()}
            with self.assertRaises(ValueError):
                mod.install(root, package)
            self.assertEqual({p: p.read_bytes() for p in root.rglob('*') if p.is_file()}, before)


if __name__ == '__main__':
    unittest.main()
