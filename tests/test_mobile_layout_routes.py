import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).parents[1]
spec=importlib.util.spec_from_file_location('layout_install',ROOT/'install.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)


class LayoutRoutes(unittest.TestCase):
    def test_rules_reach_project_and_both_weekly_workflows(self):
        rows=json.loads((ROOT/'routes.mobile-layout.json').read_text())
        targets={row['target'] for row in rows}
        self.assertTrue({'AGENTS.md','Workflows/weekly-release-and-epk-sync.md',
                         'Releases/reports/workflows/weekly-release-and-epk-sync.md',
                         'Tools/EPK Motion QA/audit_epk_layout.py','Tools/EPK Motion QA/collect_epk_layout.js',
                         'Tools/EPK Motion QA/audit_epk_evidence.py','Workflows/epk-evidence-gate.md',
                         'Workflows/epk-mobile-motion.md','Workflows/epk-responsive-layout-qa.md'} <= targets)

    def test_owned_install_preserves_unrelated_text_and_repeats(self):
        rows=json.loads((ROOT/'routes.mobile-layout.json').read_text())
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            originals={}
            for row in rows:
                target=root/row['target'];target.parent.mkdir(parents=True,exist_ok=True)
                if row['mode']=='insert':
                    originals[row['target']]=f"# Private existing file\n\n{row['anchor']}\nRetain this text.\n"
                    target.write_text(originals[row['target']],encoding='utf-8')
                elif row.get('previous_source'):
                    target.write_bytes((ROOT/row['previous_source']).read_bytes())
            module.install(root,ROOT,manifest='routes.mobile-layout.json')
            for row in rows:
                target=root/row['target']
                if row['mode']=='insert':
                    fragment=(ROOT/row['source']).read_text().strip()+'\n\n'
                    self.assertEqual(target.read_text().replace(fragment,'',1),originals[row['target']])
                else:self.assertEqual(target.read_bytes(),(ROOT/row['source']).read_bytes())
            self.assertTrue(all(row['status']=='current' for row in module.install(root,ROOT,manifest='routes.mobile-layout.json',check=True)))

    def test_modified_checker_is_not_overwritten(self):
        rows=json.loads((ROOT/'routes.mobile-layout.json').read_text())
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for row in rows:
                target=root/row['target'];target.parent.mkdir(parents=True,exist_ok=True)
                if row['mode']=='insert':target.write_text(row['anchor'])
                elif row.get('previous_source'):target.write_bytes((ROOT/row['previous_source']).read_bytes())
            checker=root/'Tools/EPK Motion QA/audit_epk_evidence.py'
            checker.write_text('Another owner changed this.\n')
            with self.assertRaises(ValueError):module.install(root,ROOT,manifest='routes.mobile-layout.json')
            self.assertEqual(checker.read_text(),'Another owner changed this.\n')
            self.assertFalse((root/'Tools/EPK Motion QA/audit_epk_layout.py').exists())


if __name__=='__main__':unittest.main()
