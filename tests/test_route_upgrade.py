import importlib.util, json, tempfile, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('upgrade',Path(__file__).resolve().parents[1]/'install.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class Upgrade(unittest.TestCase):
    def fixture(self,root,package,mode):
        root.mkdir();package.mkdir()
        old='## Managed\nOld instructions'
        new='## Managed\nNew instructions'
        (package/'old.md').write_text(old);(package/'new.md').write_text(new)
        (root/'target.md').write_text(old if mode=='copy' else '# Keep\n\n'+old+'\n\n## Anchor\nUnrelated\n')
        (package/'routes.json').write_text(json.dumps([dict(target='target.md',source='new.md',previous_source='old.md',mode=mode,anchor='## Anchor',identity='## Managed')]))
    def test_exact_prior_insert_upgrade_preserves_rest_and_repeats(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'r';package=Path(temp)/'p';self.fixture(root,package,'insert')
            mod.install(root,package)
            self.assertEqual((root/'target.md').read_text(),'# Keep\n\n## Managed\nNew instructions\n\n## Anchor\nUnrelated\n')
            self.assertEqual(mod.install(root,package)[0]['status'],'current')
    def test_copy_upgrade_requires_exact_prior_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'r';package=Path(temp)/'p';self.fixture(root,package,'copy')
            mod.install(root,package);self.assertEqual((root/'target.md').read_text(),'## Managed\nNew instructions')
    def test_edited_prior_is_a_conflict(self):
        for mode in ['insert','copy']:
            with tempfile.TemporaryDirectory() as temp:
                root=Path(temp)/'r';package=Path(temp)/'p';self.fixture(root,package,mode)
                p=root/'target.md';p.write_text(p.read_text().replace('Old instructions','Other owner edit'));before=p.read_bytes()
                with self.assertRaises(ValueError):mod.install(root,package)
                self.assertEqual(p.read_bytes(),before)
