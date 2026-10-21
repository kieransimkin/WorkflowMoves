import json
from pathlib import Path
import tempfile
import unittest
import install

PACKAGE = Path(__file__).resolve().parents[1]


class BlogworthinessRoutes(unittest.TestCase):
    def test_install_summary_preserves_all_existing_text_and_repeats(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            originals={
                'AGENTS.md':'# My Songs project instructions\n\nPrivate existing project rules.\n',
                'skill-source/project-blog-writer/SKILL.md':'# Blog\n\n## Establish the story\n\nExisting content.\n',
                '.agents/skills/project-blog-writer/SKILL.md':'# Blog\n\n## Establish the story\n\nExisting content.\n',
                'skill-source/automation-scheduling/SKILL.md':'# Scheduling\n\n## Potential problems\n\nExisting content.\n',
            }
            for name,text in originals.items():
                target=root/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text,encoding='utf-8')
            install.install(root,PACKAGE,manifest='blogworthiness-routes.json')
            before=(root/'AGENTS.md').read_bytes()
            install.install(root,PACKAGE,manifest='instruction-summary-routes.json')
            after=(root/'AGENTS.md').read_bytes()
            self.assertTrue(after.endswith(before))
            self.assertTrue(after.startswith(b'# My Songs: essential rules'))
            fragment=(PACKAGE/'fragments/blogworthiness-skill.md').read_text(encoding='utf-8').strip()+'\n\n'
            for name,text in originals.items():
                content=(root/name).read_text(encoding='utf-8')
                if name=='AGENTS.md':self.assertTrue(content.endswith(text))
                else:self.assertEqual(content.replace(fragment,'',1),text)
            for manifest in ('blogworthiness-routes.json','instruction-summary-routes.json'):
                self.assertTrue(all(row['status']=='current' for row in install.install(root,PACKAGE,check=True,manifest=manifest)))

    def test_global_rule_precedes_existing_guidance_without_replacing_it(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            original='# Visual media in all documentation\n\nRetained global rules.\n'
            (root/'AGENTS.md').write_text(original,encoding='utf-8')
            install.install(root,PACKAGE,manifest='blogworthiness-global-routes.json')
            content=(root/'AGENTS.md').read_text(encoding='utf-8')
            self.assertTrue(content.endswith(original))
            self.assertTrue(content.startswith('## Mandatory blogworthiness'))
