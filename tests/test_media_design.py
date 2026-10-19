import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("integrate_epk_media", ROOT / "tools" / "integrate_epk_media.py")
MOD = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MOD)


class MediaDesignTests(unittest.TestCase):
    def test_moves_before_footer_and_preserves_player_bytes(self):
        src = '<main><footer class="epk-footer">end</footer><section class="epk-campaign-media" aria-labelledby="campaign-media-7" style="padding:2rem"><h2 id="campaign-media-7">Campaign videos and posts</h2><p>Published videos, Shorts and campaign posts by Kieran Simkin.</p><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:1.5rem;align-items:start"><figure data-campaign-youtube="abc"><div style="aspect-ratio:16/9"><iframe src="https://www.youtube.com/embed/abc"></iframe></div><figcaption>Film</figcaption></figure></div></section></main>'
        profile = {"page_id": 7, "profile_id":"poster-7", "motif":"poster", "title":"Test", "eyebrow":"WATCH", "heading":"Watch Test", "intro":"Official campaign media.", "before_anchor":'<footer class="epk-footer">', "css":"%SECTION%{color:red}", "design_evidence":"page tokens"}
        out = MOD.transform(src, profile)
        self.assertLess(out.index('epk-campaign-media--integrated'), out.index('<footer'))
        self.assertEqual(MOD.media_bytes(src), MOD.media_bytes(out))
        self.assertIn('epk-campaign-media__item--film', out)

    def test_requires_explicit_unique_block_and_anchor(self):
        p={"page_id":1,"profile_id":"x","motif":"x","title":"x","eyebrow":"x","heading":"x","intro":"x","before_anchor":"<footer>","css":"","design_evidence":"x"}
        with self.assertRaisesRegex(ValueError, "expected one"):
            MOD.transform('<main></main>',p)

    def test_iframe_width_does_not_turn_a_portrait_short_into_a_film(self):
        src = '<main><footer></footer><section class="epk-campaign-media" aria-labelledby="campaign-media-1"><h2 id="campaign-media-1">Campaign videos and posts</h2><p>Published videos, Shorts and campaign posts by Kieran Simkin.</p><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:1.5rem;align-items:start"><figure><div style="aspect-ratio:9/16"><iframe style="width:100%"></iframe></div></figure></div></section></main>'
        p={"page_id":1,"profile_id":"x","motif":"x","title":"x","eyebrow":"x","heading":"x","intro":"x","before_anchor":"<footer>","css":"","design_evidence":"x"}
        out=MOD.transform(src,p)
        self.assertIn('epk-campaign-media__item--short',out)
        self.assertNotIn('epk-campaign-media__item--film',out)


if __name__ == '__main__': unittest.main()
