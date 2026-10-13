import unittest,importlib.util
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def module(name):
 s=importlib.util.spec_from_file_location(name,R/'tools'/(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
compose=module('compose_epk_cover');audit=module('audit_campaign_media')
W='<div class="epk-campaign-featured" data-campaign-main-video="true"><figure><div><iframe src="https://www.youtube.com/embed/ABCDEFGHIJK" title="A &amp; B" loading="eager"></iframe></div><figcaption>Watch</figcaption></figure></div>'
class CoverContract(unittest.TestCase):
 def test_artwork_retained_once_and_source_inert(self):
  img='<img src="https://example.invalid/art.png" alt="Art" width="1000" height="1000">';original='<style>.approved{color:red}</style><main>'+W+img+'<audio src="music.mp3"></audio></main><script>approved();</script>';out=compose.compose(original,'https://example.invalid/art.png','Art');self.assertEqual(out.count(img),1);self.assertIn('<template data-epk-video-template><iframe',out);self.assertIn('<audio src="music.mp3"></audio>',out);self.assertIn('<script>approved();</script>',out);self.assertNotIn('data-campaign-main-video',out);self.assertIn('aria-label="Play A &amp; B"',out)
 def test_duplicate_or_missing_composition_refused(self):
  out=compose.compose(W,'https://example.invalid/art.png','Art');self.assertRaises(ValueError,compose.compose,out,'x','x');self.assertRaises(ValueError,compose.compose,'<main></main>','x','x')
 def test_untrusted_embed_host_rejected(self):
  self.assertRaises(ValueError,compose.compose,W.replace('www.youtube.com','example.invalid'),'x','x')
 def test_video_count_and_other_shorts_preserved(self):
  extra='<iframe src="https://www.youtube.com/embed/LMNOPQRSTUV"></iframe>';out=compose.compose(W+extra,'https://example.invalid/art.png','Art');self.assertEqual(out.count('<iframe'),2);self.assertIn(extra,out)
 def test_deferred_is_distinct_from_working_playback(self):
  out=compose.compose(W,'https://example.invalid/art.png','Art');r=audit.audit([dict(epk_id=1,url='https://youtu.be/ABCDEFGHIJK',kind='video',publication_state='verified_public')],[dict(id=1,content=dict(rendered=out))]);self.assertEqual(r['items'][0]['coverage'],'deferred_embed_source_present')
 def test_ordinary_hidden_template_not_accepted(self):
  r=audit.audit([dict(epk_id=1,url='https://youtu.be/ABCDEFGHIJK',kind='video',publication_state='verified_public')],[dict(id=1,content=dict(rendered='<template><iframe src="https://www.youtube.com/embed/ABCDEFGHIJK"></iframe></template>'))]);self.assertEqual(r['items'][0]['coverage'],'missing_embed')
 def test_direct_cover_rule_keeps_scope_media_and_declarations(self):
  source='<style>@media(min-width:800px){.song .epk-cover-wrap>.epk-cover{border-radius:10px;transform:none}}</style>'
  updated=compose.extend_direct_cover_selectors(source)
  self.assertEqual(updated,'<style>@media(min-width:800px){.song .epk-cover-wrap>.epk-cover,.song .epk-cover-wrap>.epk-cover-player>.epk-cover{border-radius:10px;transform:none}}</style>')
  self.assertEqual(compose.extend_direct_cover_selectors(updated),updated)
 def test_existing_style_repair_preserves_template_and_runtime(self):
  original=compose.compose(W+'<img src="https://example.invalid/art.png">','https://example.invalid/art.png','Art')
  repaired=compose.repair_cover_styles(original)
  self.assertIn('<template data-epk-video-template><iframe',repaired)
  self.assertIn('<script data-epk-cover-runtime>',repaired)
  self.assertNotIn('bottom:auto;padding:2rem 6vw',repaired)
  self.assertIn('height:100%;max-height:100vw',repaired)
 def test_style_repair_requires_unambiguous_composed_cover(self):
  self.assertRaises(ValueError,compose.repair_cover_styles,'<main></main>')
  original=compose.compose(W,'https://example.invalid/art.png','Art')
  self.assertRaises(ValueError,compose.repair_cover_styles,original+original)
if __name__=='__main__':unittest.main()
