import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('adoption_installer', ROOT / 'install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class SharedToolAdoption(unittest.TestCase):
    def test_four_guarded_targets_preserve_other_instructions_and_are_idempotent(self):
        rows = json.loads((ROOT / 'tool-adoption-routes.json').read_text())
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[0]['target'], '.codex-relocated-home/AGENTS.md')
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            originals = {}
            for row in rows:
                path = workspace / row['target']
                path.parent.mkdir(parents=True, exist_ok=True)
                if row['mode'] == 'insert':
                    data = ('Keep this private prefix\r\n\r\n' + row['anchor']
                            + '\r\nKeep this private suffix\r\n').encode()
                    originals[row['target']] = data
                else:
                    data = (ROOT / row['previous_source']).read_bytes()
                path.write_bytes(data)
            self.assertTrue(all(r['status'] == 'pending' for r in installer.install(
                workspace, ROOT, check=True, manifest='tool-adoption-routes.json')))
            installer.install(workspace, ROOT, manifest='tool-adoption-routes.json')
            for row in rows:
                if row['mode'] == 'insert':
                    data = (workspace / row['target']).read_bytes()
                    snippet = (ROOT / row['source']).read_text().strip().replace('\n', '\r\n').encode()
                    self.assertEqual(data.replace(snippet + b'\r\n\r\n', b'', 1), originals[row['target']])
            self.assertTrue(all(r['status'] == 'current' for r in installer.install(
                workspace, ROOT, check=True, manifest='tool-adoption-routes.json')))

    def test_unreviewed_renderer_routing_edit_stops_before_installation(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            for row in json.loads((ROOT / 'tool-adoption-routes.json').read_text()):
                path = workspace / row['target']
                path.parent.mkdir(parents=True, exist_ok=True)
                if row['mode'] == 'insert':
                    path.write_text(row['anchor'] + '\n')
                else:
                    path.write_bytes((ROOT / row['previous_source']).read_bytes())
            target = workspace / 'Workflows/scheduled-danceflow-tool-use.md'
            target.write_bytes(target.read_bytes() + b'\n| **FrameRudiments** | Another owner changed this managed row. |\n')
            original_global = (workspace / '.codex-relocated-home/AGENTS.md').read_bytes()
            with self.assertRaisesRegex(ValueError, 'Existing managed block differs'):
                installer.install(workspace, ROOT, manifest='tool-adoption-routes.json')
            self.assertEqual((workspace / '.codex-relocated-home/AGENTS.md').read_bytes(), original_global)
