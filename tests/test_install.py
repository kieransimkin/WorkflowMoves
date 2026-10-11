import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('workflow_install', Path(__file__).resolve().parents[1] / 'install.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class WorkflowInstallation(unittest.TestCase):
    def test_equivalent_existing_newline_styles_do_not_rewrite(self):
        text = '## Managed\nAlready present\n\n## Anchor\r\nUnrelated\r\n'
        self.assertEqual(mod.merge(text, '## Managed\r\nAlready present', '## Anchor', '## Managed', '\r\n'), text)

    def test_insert_preserves_original_and_repeat_is_exact(self):
        original = '# Existing\n\nPrivate untouched text\n\n## Anchor\nOriginal details\n'
        snippet = '## Managed\n\nNew instructions'
        updated = mod.merge(original, snippet, '## Anchor', '## Managed')
        self.assertEqual(updated.replace(snippet + '\n\n', '', 1), original)
        self.assertEqual(mod.merge(updated, snippet, '## Anchor', '## Managed'), updated)

    def test_refuses_modified_block_and_ambiguous_anchor(self):
        with self.assertRaises(ValueError):
            mod.merge('## Managed\nAltered\n## Anchor', '## Managed\nExpected', '## Anchor', '## Managed')
        with self.assertRaises(ValueError):
            mod.merge('## Anchor\n## Anchor', '## Managed', '## Anchor', '## Managed')

    def test_refuses_paths_outside_root(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                mod.contained(Path(temp), '../outside.md')

    def test_preflight_conflict_writes_nothing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'workspace'
            package = Path(temp) / 'package'
            root.mkdir(); package.mkdir()
            (root/'a.md').write_text('## Anchor\nKeep\n')
            (root/'b.md').write_text('## Managed\nDifferent\n## Anchor\n')
            (package/'fragment.md').write_text('## Managed\nExpected\n')
            rows = [{'target':p,'source':'fragment.md','mode':'insert','anchor':'## Anchor','identity':'## Managed'} for p in ('a.md','b.md')]
            (package/'routes.json').write_text(json.dumps(rows))
            before = (root/'a.md').read_bytes()
            with self.assertRaises(ValueError):
                mod.install(root, package)
            self.assertEqual((root/'a.md').read_bytes(), before)

    def test_bom_mixed_newlines_and_two_routes_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'workspace'; package = Path(temp) / 'package'
            root.mkdir(); package.mkdir()
            original = b'\xef\xbb\xbf# Original\r\nLone LF\n\r\n## Anchor\r\nKeep\r\n'
            (root/'a.md').write_bytes(original)
            (package/'one.md').write_text('## One\nNew one\n')
            (package/'two.md').write_text('## Two\nNew two\n')
            rows = [{'target':'a.md','source':s,'mode':'insert','anchor':'## Anchor','identity':i} for s,i in [('one.md','## One'),('two.md','## Two')]]
            (package/'routes.json').write_text(json.dumps(rows))
            mod.install(root, package)
            data = (root/'a.md').read_bytes()
            for snippet in ('## One\r\nNew one\r\n\r\n','## Two\r\nNew two\r\n\r\n'):
                data = data.replace(snippet.encode(),b'',1)
            self.assertEqual(data, original)
            self.assertTrue(all(r['status']=='current' for r in mod.install(root,package,check=True)))


if __name__ == '__main__':
    unittest.main()
