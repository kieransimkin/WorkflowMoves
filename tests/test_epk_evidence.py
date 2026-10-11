import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('epk_evidence', Path(__file__).parents[1]/'tools/audit_epk_evidence.py')
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

def record():
    return {'page_id': 'example', 'widths': [{'width':w,'overflow':False} for w in (390,900,1440)],
            'motion': {'required_consumers':['hero'], 'routes':[{'consumer':'hero','controller':'example:hero',
              'sensor_owner_count':1,'evidence_kind':'synthetic','sample':{'x':.8,'y':-.6},
              'visual_before':'matrix-neutral','visual_after':'matrix-moved','extent_within_bounds':True,
              'desktop_pointer_preserved':True,'resets':{name:{'x':0,'y':0} for name in module.RESETS}}]},
            'timing': {'configured':{'lyric':'https://example.test/a%20b.lrc?version=2'}, 'hardcoded_literals':[],
              'metadata_only_change_proved':True,'consumers':[{'id':'lyrics','kind':'lyric','resolved_url':'https://example.test/a%20b.lrc?version=2','state':'ready','parsed_count':12}]}}

class EvidenceTests(unittest.TestCase):
    def test_complete_synthetic_is_not_physical_certification(self):
        result=module.audit(record()); self.assertEqual(result['status'],'passed'); self.assertFalse(result['physical_sensor_delivery_certified'])
    def test_partial_sensor_attachment_fails(self):
        r=record(); r['motion']['required_consumers'].append('below-fold-card'); self.assertEqual(module.audit(r)['status'],'failed')
    def test_duplicate_sensor_route_fails(self):
        r=record(); r['motion']['routes'].append(copy.deepcopy(r['motion']['routes'][0])); self.assertEqual(module.audit(r)['status'],'failed')
    def test_listener_without_painted_response_fails(self):
        r=record(); r['motion']['routes'][0]['visual_after']='matrix-neutral'; self.assertEqual(module.audit(r)['status'],'failed')
    def test_nonfinite_and_unbounded_inputs_fail(self):
        for value in (float('nan'),float('inf'),2,True):
            r=record(); r['motion']['routes'][0]['sample']['x']=value; self.assertEqual(module.audit(r)['status'],'failed')
    def test_missing_lifecycle_reset_fails(self):
        r=record(); del r['motion']['routes'][0]['resets']['hidden']; self.assertEqual(module.audit(r)['status'],'failed')
    def test_exact_query_encoding_is_preserved(self):
        for value in ('https://example.test/a b.lrc?version=2','https://example.test/a%20b.lrc?version=1'):
            r=record(); r['timing']['consumers'][0]['resolved_url']=value; self.assertEqual(module.audit(r)['status'],'failed')
    def test_wrong_multitrack_association_fails(self):
        r=record(); r['timing']['multi_track']=True; self.assertEqual(module.audit(r)['status'],'failed')
    def test_exact_multitrack_mapping_passes(self):
        r=record(); r['timing']['multi_track']=True; r['timing']['tracks']={'master-a':r['timing']['configured']}; r['timing']['consumers'][0]['track']='master-a'; self.assertEqual(module.audit(r)['status'],'passed')
    def test_missing_metadata_safe_fallback(self):
        r=record(); r['timing']={'configured':{},'hardcoded_literals':[],'consumers':[{'id':'lyrics','kind':'lyric','state':'unavailable','download_disabled':True,'audio_and_readable_lyrics_retained':True}]}; self.assertEqual(module.audit(r)['status'],'passed')
    def test_missing_source_scan_is_not_zero(self):
        r=record(); del r['timing']['hardcoded_literals']; self.assertEqual(module.audit(r)['status'],'failed')
    def test_boolean_owner_count_is_not_one(self):
        r=record(); r['motion']['routes'][0]['sensor_owner_count']=True; self.assertEqual(module.audit(r)['status'],'failed')
    def test_hardcoded_fallback_and_missing_metadata_switch_fail(self):
        for change in ({'hardcoded_literals':['old.lrc']},{'metadata_only_change_proved':False}):
            r=record(); r['timing'].update(change); self.assertEqual(module.audit(r)['status'],'failed')
    def test_static_pages_require_reason(self):
        r=record(); r['motion']={'intentional_static_reason':'No spatial consumer; ordinary button hover only'}; self.assertEqual(module.audit(r)['status'],'passed'); r['motion']={}; self.assertEqual(module.audit(r)['status'],'failed')
    def test_missing_layout_evidence_fails(self):
        r=record(); r['widths'].pop(); self.assertEqual(module.audit(r)['status'],'failed')

if __name__ == '__main__': unittest.main()
