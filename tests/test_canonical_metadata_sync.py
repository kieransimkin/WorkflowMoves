import importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('metadata_sync_install',ROOT/'install.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class CanonicalMetadataSync(unittest.TestCase):
 def test_routes_cover_project_and_both_weekly_workflows(self):
  routes=[r for r in json.loads((ROOT/'routes.json').read_text()) if r['source']=='rules/canonical-metadata-wordpress-sync.md']
  self.assertEqual({r['target'] for r in routes},{'AGENTS.md','Workflows/weekly-release-and-epk-sync.md','Releases/reports/workflows/weekly-release-and-epk-sync.md','Workflows/canonical-song-metadata-wordpress-sync.md'})
 def test_same_job_preservation_and_approval_contract(self):
  text=(ROOT/'rules/canonical-metadata-wordpress-sync.md').read_text()
  for phrase in ['BPM, lyric timing, cue timing','during the same job','local canonical record alone','only timing-file authority','mandatory tool/action-time approval','already granted approval','SHA-256','reload the editor','anonymous public configuration','private masters']:
   self.assertIn(phrase.lower(),text.lower())
 def test_install_is_additive_idempotent_and_conflict_safe(self):
  snippet=(ROOT/'rules/canonical-metadata-wordpress-sync.md').read_text().strip()
  original='# User content\n\n## WordPress metadata is the only EPK timing-file authority\nKeep timing rules\n'
  result=mod.merge(original,snippet,'## WordPress metadata is the only EPK timing-file authority','## Synchronize canonical song metadata into WordPress')
  self.assertEqual(result.replace(snippet+'\n\n','',1),original)
  self.assertEqual(mod.merge(result,snippet,'## WordPress metadata is the only EPK timing-file authority','## Synchronize canonical song metadata into WordPress'),result)
  with self.assertRaises(ValueError):mod.merge(result.replace('same job','different job'),snippet,'## WordPress metadata is the only EPK timing-file authority','## Synchronize canonical song metadata into WordPress')

