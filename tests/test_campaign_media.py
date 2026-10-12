import importlib.util, unittest
from pathlib import Path
s=importlib.util.spec_from_file_location('media',Path(__file__).resolve().parents[1]/'tools/audit_campaign_media.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
ID='abcDEfg_123'
def item(url=None,**kw):
    return dict(epk_id=1,url=url or 'https://youtube.com/shorts/'+ID,kind='short',publication_state='verified_public',**kw)
def page(body):return [dict(id=1,content={'rendered':body})]
class Coverage(unittest.TestCase):
    def test_watch_short_embed_identity(self):
        self.assertEqual(m.identity('https://youtu.be/'+ID+'?t=10'),m.identity('https://youtube.com/shorts/'+ID))
        self.assertEqual(m.audit([item()],page('<iframe src="https://www.youtube-nocookie.com/embed/'+ID+'"></iframe>'))['items'][0]['coverage'],'embedded_source_present')
    def test_hidden_metadata_and_script_are_not_embeds(self):
        for body in ['<script><iframe src="https://youtube.com/embed/'+ID+'"></iframe></script>','<div hidden><iframe src="https://youtube.com/embed/'+ID+'"></iframe></div>','<meta content="https://youtube.com/embed/'+ID+'">']:
            self.assertEqual(m.audit([item()],page(body))['items'][0]['coverage'],'missing_embed')
    def test_proven_crossposts_choose_youtube_once(self):
        rows=[item('https://instagram.com/reel/x',asset_group='hash:one'),item(asset_group='hash:one')]
        found=m.audit(rows,page(''))['items'];self.assertEqual(len(found),1);self.assertTrue(found[0]['url'].startswith('https://youtube.com'));self.assertEqual(found[0]['deduplicated'],1)
    def test_distinct_and_scheduled_never_collapse(self):
        scheduled=item();scheduled['publication_state']='scheduled'
        rows=[item(asset_group='one'),item('https://youtube.com/shorts/ZbcDEfg_123',asset_group='two'),scheduled]
        self.assertEqual(len(m.audit(rows,page(''))['items']),3)
        self.assertIn('needs_publication_verification',[x['coverage'] for x in m.audit(rows,page(''))['items']])
    def test_restricted_item_requires_link(self):
        x=item(embed_blocked_reason='age restricted')
        self.assertEqual(m.audit([x],page(''))['items'][0]['coverage'],'missing_native_fallback')
        self.assertEqual(m.audit([x],page('<a href="'+x['url']+'">Watch</a>'))['items'][0]['coverage'],'missing_native_fallback')
    def test_native_fallback_requires_exact_source_evidence(self):
        x=item(embed_blocked_reason='Embedding denied',wordpress_url='https://artist.example/clip.mp4',source_hash_verified=True)
        self.assertEqual(m.audit([x],page('<video src="https://artist.example/clip.mp4"></video>'))['items'][0]['coverage'],'native_fallback_source_present')
        x['source_hash_verified']=False
        self.assertEqual(m.audit([x],page('<video src="https://artist.example/clip.mp4"></video>'))['items'][0]['coverage'],'missing_native_fallback')
    def test_unavailable_and_invalid_inputs(self):
        self.assertEqual(m.audit([item()],[])['items'][0]['coverage'],'epk_unavailable')
        with self.assertRaises(ValueError):m.audit([{}],[])
