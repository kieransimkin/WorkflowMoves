import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('timing', Path(__file__).resolve().parents[1] / 'tools/audit_epk_timing_bindings.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class TimingBindings(unittest.TestCase):
    def test_metadata_only_and_dynamic_reference_pass(self):
        text = '<script id="dance-moves-core-js-extra">var danceMovesConfig={"lyricTimingUrl":"https://example.test/a.lrc"};</script><script>fetch(window.danceMovesConfig.lyricTimingUrl)</script>'
        self.assertEqual(mod.audit(text), [])

    def test_absolute_relative_and_signed_literals(self):
        for value in ('https://example.test/a.lrc?signature=abc%2Fdef', '/files/a.cue', './song.lrc'):
            hits = mod.audit('<a href="' + value + '" download>Timing</a>')
            self.assertEqual(hits[0]['url'], value)

    def test_json_attribute_and_known_json_script_source(self):
        value = 'https://example.test/cues.json?token=a%2Fb'
        self.assertEqual(mod.audit('<audio data-cue-url="' + value + '"></audio>')[0]['url'], value)
        self.assertEqual(mod.audit('<script>fetch("' + value + '")</script>', [value])[0]['url'], value)

    def test_does_not_exempt_custom_head_script(self):
        self.assertEqual(len(mod.audit('<head><script>fetch("/a.lrc")</script></head>')), 1)

    def test_encoded_url_preserved_and_unrelated_assets_allowed(self):
        self.assertEqual(mod.audit('<audio src="/song.mp3"></audio><img src="/cover.jpg">'), [])
        self.assertEqual(mod.audit('<a href="/timing.lrc?a=1&amp;b=2">LRC</a>')[0]['url'], '/timing.lrc?a=1&b=2')

if __name__ == '__main__':
    unittest.main()
