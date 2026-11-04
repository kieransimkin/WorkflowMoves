import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location('social_install', ROOT / 'install.py')
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class SocialRoutesTests(unittest.TestCase):
    def test_install_preserves_surrounding_content_and_repeat_is_idempotent(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.routes = json.loads((ROOT / 'social-scheduling-routes.json').read_text(encoding='utf-8'))
            originals = {}
            for row in self.routes:
                if row['mode'] != 'insert':
                    continue
                target = row['target']
                original = ('# Existing\r\n\r\nPrivate notes preserved.\r\n\r\n' + row['anchor'] + '\r\nKnown issue.\r\n').encode()
                p = root / target
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(original)
                originals[target] = original
            preview = M.install(root, check=True, manifest='social-scheduling-routes.json')
            self.assertEqual(len(preview), 7)
            self.assertTrue(all(r['status'] == 'pending' for r in preview))
            self.assertFalse((root / 'Tools/social_schedule_plan.py').exists())
            M.install(root, manifest='social-scheduling-routes.json')
            for row in self.routes:
                if row['mode'] != 'insert':
                    continue
                content = (root / row['target']).read_bytes()
                snippet = (ROOT / row['source']).read_text().strip().replace('\n', '\r\n').encode()
                self.assertEqual(content.replace(snippet + b'\r\n\r\n', b''), originals[row['target']])
            self.assertTrue(all(r['status'] == 'current' for r in M.install(root, manifest='social-scheduling-routes.json')))

    def test_recovery_skill_and_native_persistence_guidance_ship(self):
        skill = (ROOT / 'skills/direct-social-scheduling/SKILL.md').read_text(encoding='utf-8')
        workflow = (ROOT / 'workflows/direct-social-scheduling.md').read_text(encoding='utf-8')
        self.assertTrue(skill.startswith('---\nname: direct-social-scheduling\n'))
        self.assertIn('interrupted-session recovery', skill)
        self.assertIn('Recover and prove native persistence', workflow)
        self.assertIn('visually populated framework field could persist as blank', workflow)
