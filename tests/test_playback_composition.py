import unittest,importlib.util,copy
from pathlib import Path
root=Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location('playback',root/'tools/compose_epk_playback.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
BASE={'master':{'id':'isrc:TEST00000001','duration':120,'urls':['https://kieransimkin.co.uk/wp-content/uploads/2026/01/master.mp3']},'players':[{'kind':'youtube','id':'ABCDEFGHIJK','offset':48,'duration':20,'playerStart':0,'masterVerified':True}]}
class PlaybackComposition(unittest.TestCase):
 def test_preserves_complete_source_and_attaches_explicit_mapping(self):
  source='<main><audio src="approved.mp3"></audio></main><style>.approved{color:red}</style><script>approved();</script>';out=module.compose(source,BASE);self.assertTrue(out.startswith(source));self.assertIn('"offset":48',out);self.assertIn('data-epk-player-bindings',out);self.assertIn('registerYouTube',out)
 def test_duplicate_and_unverified_sources_are_refused(self):
  config=copy.deepcopy(BASE);config['players'].append(config['players'][0].copy());self.assertRaises(ValueError,module.validate,config);config=copy.deepcopy(BASE);config['players'][0]['masterVerified']=False;self.assertRaises(ValueError,module.validate,config)
 def test_out_of_master_or_nonfinite_windows_are_refused(self):
  for offset,duration in [(-1,20),(110,20),(48,0),(float('nan'),20),(48,float('inf'))]:
   config=copy.deepcopy(BASE);config['players'][0].update(offset=offset,duration=duration);self.assertRaises(ValueError,module.validate,config)
 def test_private_configuration_and_duplicate_composition_are_refused(self):
  config=copy.deepcopy(BASE);config['master']['source_path']='private/master.wav';self.assertRaises(ValueError,module.validate,config);out=module.compose('<main></main>',BASE);self.assertRaises(ValueError,module.compose,out,BASE)
 def test_script_closing_text_is_encoded_as_inert_json(self):
  config=copy.deepcopy(BASE);config['master']['id']='</script><script>alert(1)</script>';out=module.compose('<main></main>',config);self.assertNotIn(config['master']['id'],out);self.assertIn('\\u003c/script>',out)
if __name__=='__main__':unittest.main()
