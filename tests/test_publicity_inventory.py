import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('publicity_inventory', Path(__file__).parents[1] / 'tools/publicity_inventory.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PublicityInventoryTests(unittest.TestCase):
    def test_missing_root_cannot_look_like_an_empty_audit(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, 'existing directory'):
                module.inventory(Path(folder) / 'missing')

    def test_published_outcome_link_is_still_only_a_candidate(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'ledger.md').write_text('Published outcome: https://example.test/item\n', encoding='utf-8')
            result = module.inventory(root)
            self.assertTrue(result['candidates'][0]['matches'][0]['strong_candidate'])
            self.assertEqual(result['candidates'][0]['state'], 'candidate_detected')

    def test_promises_and_negations_never_become_verified(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'plan.md').write_text('No verified airplay.\nPromised playlist placement.\nArticle published yesterday.\n', encoding='utf-8')
            result = module.inventory(root)
            self.assertEqual(result['candidates'][0]['state'], 'candidate_detected')
            self.assertEqual(len(result['candidates'][0]['matches']), 3)
            self.assertEqual(result['candidates'][0]['matches'][2]['line'], 3)

    def test_invalid_utf8_is_explicit_and_source_bytes_are_unchanged(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            original = b'published\xff'
            (root / 'bad.md').write_bytes(original)
            result = module.inventory(root)
            self.assertEqual(len(result['unavailable']), 1)
            self.assertEqual((root / 'bad.md').read_bytes(), original)

    def test_embedded_source_and_generated_timing_are_excluded(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ['repo', 'cue-generation-private']:
                (root / name).mkdir()
                (root / name / 'README.md').write_text('published', encoding='utf-8')
            (root / 'repo/.git').mkdir()
            result = module.inventory(root)
            self.assertEqual(result['files'], [])
            self.assertEqual(set(result['skipped_directories']), {'repo', 'cue-generation-private'})

    def test_long_lines_report_truncation_with_source_hash(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'plan.md').write_text('published ' + 'x' * 3000, encoding='utf-8')
            result = module.inventory(root)
            self.assertTrue(result['candidates'][0]['matches'][0]['truncated'])
            self.assertEqual(len(result['files'][0]['sha256']), 64)
