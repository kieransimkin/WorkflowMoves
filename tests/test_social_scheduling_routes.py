import importlib.util
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
            targets = ['Workflows/release-video-social-scheduling.md', 'skill-source/social-video-scheduling/SKILL.md']
            original = b'# Existing\r\n\r\nPrivate notes preserved.\r\n\r\n## Potential problems\r\nKnown issue.\r\n'
            for target in targets:
                p = root / target
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(original)
            preview = M.install(root, check=True, manifest='social-scheduling-routes.json')
            self.assertTrue(all(r['status'] == 'pending' for r in preview))
            self.assertFalse((root / 'Tools/social_schedule_plan.py').exists())
            M.install(root, manifest='social-scheduling-routes.json')
            for target in targets:
                content = (root / target).read_bytes()
                snippet = (ROOT / 'fragments/direct-social-scheduling.md').read_text().strip().replace('\n', '\r\n').encode()
                self.assertEqual(content.replace(snippet + b'\r\n\r\n', b''), original)
            self.assertTrue(all(r['status'] == 'current' for r in M.install(root, manifest='social-scheduling-routes.json')))
