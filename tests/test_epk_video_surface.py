import importlib.util
import sys
import unittest
from pathlib import Path

TOOLS=Path(__file__).resolve().parents[1]/'tools'
sys.path.insert(0,str(TOOLS))
from repair_epk_video_surface import repair,verify_preservation,native_runtime
from compose_epk_cover import runtime_text


class VideoSurfaceRepairTests(unittest.TestCase):
    cover='<div class="epk-cover-player" data-epk-cover-player="abcdefghijk"><img src="cover.jpg"><button data-epk-video-play>Play</button><div data-epk-video-slot hidden></div><button data-epk-video-close hidden>Close</button><template data-epk-video-template><iframe src="https://www.youtube.com/embed/abcdefghijk" title="A video"></iframe></template></div><script data-epk-cover-runtime>old();</script>'
    frame='<iframe src="https://www.youtube-nocookie.com/embed/abcdefghijk" title="A &amp; B" allow="fullscreen"></iframe>'

    def check(self,before,profile):
        after,edits=repair(before,profile)
        verify_preservation(before,after,edits)
        second,again=repair(after,profile)
        self.assertEqual(after,second)
        self.assertEqual([],again)
        return after

    def test_cover_preserves_unicode_crlf_and_binding(self):
        prefix='<h1>Crimson — 漢字</h1>\r\n<script type="application/json">{"offset":42.4}</script>\r\n'
        after=self.check(prefix+self.cover,{'cover':True})
        self.assertTrue(after.startswith(prefix))
        self.assertIn('pointer-events:auto;cursor:pointer',after)
        self.assertIn('epkCoverOwner="2"',after)

    def test_provider_keeps_exact_iframe_and_siblings(self):
        after=self.check('<aside>unchanged</aside>'+self.frame+'<footer>unchanged</footer>',{'provider_starts':[{'id':'abcdefghijk','poster':'https://example.com/poster.jpg'}]})
        self.assertIn('<template data-epk-video-template>'+self.frame+'</template>',after)
        self.assertIn('epk-video-picture',after)
        self.assertNotIn('data-epk-video-close',after.split('<template')[0])

    def test_native_explicit_source_only(self):
        before='<video controls poster="cover.jpg"><source src="https://example.com/a.mp4"></video><video controls src="https://example.com/b.mp4"></video>'
        after=self.check(before,{'native_sources':['https://example.com/a.mp4']})
        self.assertTrue(after.startswith(before))
        self.assertIn('"sources":["https://example.com/a.mp4"]',after)

    def test_fail_closed_ambiguous_and_missing(self):
        for source,profile in [(self.frame*2,{'provider_starts':[{'id':'abcdefghijk','poster':'https://example.com/a.jpg'}]}),('',{'cover':True}),('',{'native_sources':['https://example.com/missing.mp4']}),(self.cover,{'unknown':True})]:
            with self.subTest(profile=profile):
                with self.assertRaises(ValueError):repair(source,profile)

    def test_unsafe_urls_rejected(self):
        for profile in [{'native_sources':['javascript:alert(1)']},{'provider_starts':[{'id':'abcdefghijk','poster':'http://example.com/a.jpg'}]}]:
            with self.assertRaises(ValueError):repair(self.frame,profile)

    def test_wordpress_safe_runtime(self):
        for code in (runtime_text(),native_runtime()):
            self.assertNotIn('<',code)
            self.assertNotIn('&',code)
            self.assertNotIn('\n',code)

    def test_reverse_proof_detects_unrelated_changes(self):
        after,edits=repair(self.cover,{'cover':True})
        with self.assertRaises(ValueError):verify_preservation(self.cover,after+'unreviewed',edits)


if __name__=='__main__':unittest.main()
