import unittest
from tools import clean_epk_video_links as m

VIDEO = 'https://www.youtube.com/embed/ABCDEFGHIJK'
WATCH = 'https://www.youtube.com/watch?v=ABCDEFGHIJK'
FRAME = '<iframe title="Song" src="' + VIDEO + '"></iframe>'
LINK = '<a href="' + WATCH + '">Song &amp; story — watch on YouTube</a>'


class LinkCleanup(unittest.TestCase):
    def test_caption_title_and_all_non_target_bytes_survive(self):
        source = ('<style>approved()</style><figure>' + FRAME +
                  '<figcaption>' + LINK + '</figcaption></figure>' +
                  '<script>approved()</script>\n<p>Unicode: آزادی 🎵</p>')
        result, edits = m.clean(source)
        self.assertEqual(result, source.replace(LINK, 'Song &amp; story'))
        self.assertEqual(len(edits), 1)
        self.assertEqual(m.clean(result), (result, []))

    def test_styled_buttons_are_preserved_even_with_watch_label(self):
        button = LINK.replace('<a ', '<a class="release-button" ')
        source = '<figure>' + FRAME + '<figcaption>' + button + '</figcaption></figure>'
        self.assertEqual(m.clean(source), (source, []))

    def test_cover_template_and_player_controls_survive(self):
        link = '<a class="epk-cover-player__watch" href="' + WATCH + '">Watch on YouTube</a>'
        source = '<div><div data-epk-cover-player="ABCDEFGHIJK"><img src="art.png"><button>Play</button><template>' + FRAME + '</template></div>' + link + '</div>'
        self.assertEqual(m.clean(source)[0], source.replace(link, ''))

    def test_link_only_or_mismatched_fallback_is_preserved(self):
        for source in [LINK, '<figure><figcaption>' + LINK + '</figcaption></figure>',
                       '<figure>' + FRAME.replace('ABCDEFGHIJK', 'LMNOPQRSTUV') + '<figcaption>' + LINK + '</figcaption></figure>']:
            self.assertEqual(m.clean(source), (source, []))

    def test_post_citation_disclosure_and_other_links_survive(self):
        citation = '<a href="' + WATCH + '">Original YouTube Short (age confirmation required)</a>'
        source = '<figure>' + FRAME + '<figcaption>Explicit lyrics. ' + citation + ' ' + LINK + '</figcaption></figure>'
        self.assertEqual(m.clean(source)[0], source.replace(LINK, 'Song &amp; story'))

    def test_native_replacement_uses_exact_proven_asset_marker(self):
        source = '<figure data-campaign-native="youtube:ABCDEFGHIJK"><video controls src="original.mp4"></video><figcaption>' + LINK + '</figcaption></figure>'
        self.assertEqual(m.clean(source)[0], source.replace(LINK, 'Song &amp; story'))

    def test_script_literals_are_not_treated_as_links(self):
        source = '<script>const example=' + repr('<figure>' + FRAME + '<figcaption>' + LINK + '</figcaption></figure>') + ';</script>'
        self.assertEqual(m.clean(source), (source, []))


if __name__ == '__main__':
    unittest.main()
