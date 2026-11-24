"""Synthetic acceptance cases for report identity, temporal and publication safety."""
import copy,hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('shorts_report',P/'tools/shorts_report.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ShortsReportTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.p=Path(self.tmp.name)
        self.e=self.p/'native.json';self.e.write_text('{"synthetic":true}')
        self.baseline=self.p/'dataset.json';self.baseline.write_text(json.dumps({'TikTok':[{'id':'a','caption':'Synthetic baseline','views':100,'new_followers':0,'observed_at':'2026-11-24T10:00:00+00:00'}]}))
        self.report=self.p/'baseline.md';self.report.write_text('# Synthetic historical report')
        self.cfg={'artist':'Example Artist','accounts':{'TikTok':['@example']},'evidence_root':str(self.p),'report_root':str(self.p/'report'),'baseline_dataset':str(self.baseline),'baseline_report':str(self.report)}
        self.o={'schema':m.SCHEMA,'artist':'Example Artist','platform':'TikTok','account':'@example','run_id':'run1','observed_at':'2026-11-24T12:00:00+00:00','status':'measured','coverage':{'scope':'Synthetic fixture','complete':False},'source':{'path':str(self.e),'sha256':m.digest(self.e)},'posts':[{'id':'a','title':'Synthetic newer observation','publication_state':'published','format_status':'candidate','metrics':{'views':{'value':120,'definition':'tiktok.views','unit':'count','window':{'kind':'lifetime','cutoff':'2026-11-24T11:00:00+00:00'}}}}]}
    def test_artist_and_account_are_guarded(self):
        for field,value in [('artist','Other Artist'),('account','@other')]:
            o=copy.deepcopy(self.o);o[field]=value
            with self.assertRaises(ValueError):m.validate(self.cfg,o)
    def test_changed_evidence_is_rejected(self):
        self.e.write_text('changed')
        with self.assertRaises(ValueError):m.validate(self.cfg,self.o)
    def test_scheduled_and_invented_geometry_are_rejected(self):
        for field,value in [('publication_state','scheduled'),('format_status','confirmed_9_16')]:
            o=copy.deepcopy(self.o);o['posts'][0][field]=value
            with self.assertRaises(ValueError):m.validate(self.cfg,o)
    def test_identical_replay_is_idempotent_but_conflicting_run_is_held(self):
        self.assertEqual('saved',m.ingest(self.cfg,self.o)['state']);self.assertEqual('already_saved',m.ingest(self.cfg,self.o)['state'])
        o=copy.deepcopy(self.o);o['posts'][0]['metrics']['views']['value']=121
        with self.assertRaises(ValueError):m.ingest(self.cfg,o)
    def test_old_cutoff_cannot_replace_newer_data(self):
        m.ingest(self.cfg,self.o);o=copy.deepcopy(self.o);o['run_id']='run2';o['observed_at']='2026-11-24T13:00:00+00:00';o['posts'][0]['metrics']['views'].update(value=90,window={'kind':'lifetime','cutoff':'2026-11-24T09:00:00+00:00'});m.ingest(self.cfg,o)
        rows,_=m.assemble(self.cfg);self.assertEqual(120,rows[0]['metrics']['views']['value'])
    def test_period_does_not_overwrite_lifetime(self):
        o=copy.deepcopy(self.o);o['posts'][0]['metrics']['views'].update(value=4,window={'kind':'period','start':'2026-11-20','end':'2026-11-23'});m.ingest(self.cfg,o)
        rows,_=m.assemble(self.cfg);self.assertEqual(100,rows[0]['metrics']['views']['value']);self.assertEqual(2,len(rows[0]['series']['views']))
    def test_revised_lower_count_is_preserved_without_growth_invention(self):
        self.o['posts'][0]['metrics']['views']['value']=95;m.ingest(self.cfg,self.o);rows,_=m.assemble(self.cfg);self.assertEqual(95,rows[0]['metrics']['views']['value'])
    def test_unknown_remains_null_and_no_exposure_is_invented(self):
        self.o['posts'][0]['metrics']['views']['value']=None;m.ingest(self.cfg,self.o);rows,_=m.assemble(self.cfg);self.assertIsNone(rows[0]['metrics']['views']['value'])
        o=copy.deepcopy(self.o);o.update(run_id='held',status='unavailable',posts=[],observed_at='2026-11-24T13:00:00+00:00');m.ingest(self.cfg,o);self.assertEqual('unavailable',m.assemble(self.cfg)[1][-1]['status'])
    def test_owned_lock_cannot_be_recovered(self):
        root=Path(self.cfg['report_root']);root.mkdir();lock=root/'report-writer.lock';lock.write_text('{"token":"other-owner"}')
        with self.assertRaises(ValueError):m.ingest(self.cfg,self.o)
        self.assertEqual('other-owner',json.loads(lock.read_text())['token'])
    def test_publish_retains_baseline_and_unchanged_publish_is_noop(self):
        before=m.digest(self.baseline);m.ingest(self.cfg,self.o);r=m.publish(self.cfg);self.assertEqual('published_local',r['state']);self.assertEqual(before,m.digest(self.baseline))
        manifest=m.read(Path(r['path'])/'manifest.json')
        for n,h in manifest['files'].items():self.assertEqual(h,m.digest(Path(r['path'])/n))
        self.assertEqual('already_current',m.publish(self.cfg)['state'])
    def test_bad_units_nonfinite_and_inflated_full_watch_rejected(self):
        for field,value in [('unit','seconds'),('value',float('inf'))]:
            o=copy.deepcopy(self.o);o['posts'][0]['metrics']['views'][field]=value
            with self.assertRaises(ValueError):m.validate(self.cfg,o)
        o=copy.deepcopy(self.o);o['posts'][0]['metrics']={'completion_percent':{'value':105,'unit':'percent','definition':'tiktok.completion_percent','window':{'kind':'lifetime','cutoff':'2026-11-24'}}}
        with self.assertRaises(ValueError):m.validate(self.cfg,o)
    def test_identical_timestamp_conflict_is_not_silently_chosen(self):
        m.ingest(self.cfg,self.o);o=copy.deepcopy(self.o);o['run_id']='run2';o['posts'][0]['metrics']['views']['value']=121;m.ingest(self.cfg,o)
        with self.assertRaises(ValueError):m.assemble(self.cfg)
if __name__=='__main__':unittest.main()
