import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'tools'))
from audit_epk_youtube_flow import WIDTHS, audit


def rect(left, right, top, bottom):
    return dict(left=left, right=right, top=top, bottom=bottom)


def observation(width, playing=False, restored=False):
    wide = width >= 760
    copy = rect(200, 300, 50, 100) if wide else rect(20, 300, 300, 340)
    return dict(video_id='FgQ6IXRrk4c', viewport_width=width, horizontal_overflow=False,
                frame_count=int(playing), frame=rect(20, 180, 50, 140) if playing else None,
                poster=None if playing else rect(20, 140, 50, 170),
                opener=None if playing else rect(40, 80, 70, 110),
                close=rect(120, 160, 145, 185) if playing else None,
                copy={'h1': copy}, following_selector='#overview', following=rect(20, 300, 380, 460),
                focus_on_opener=restored)


def evidence():
    return {'widths': [
        {'width': w, 'youtube_cover_ids': ['FgQ6IXRrk4c'], 'youtube_reveals': [{
            'player': '#hero-video', 'video_id': 'FgQ6IXRrk4c', 'input': 'touch' if w <= 430 else 'mouse',
            'states': dict(idle=observation(w), playing=observation(w, playing=True),
                           restored=observation(w, restored=True)),
        }]} for w in WIDTHS
    ]}


class YouTubeFlowTests(unittest.TestCase):
    def test_same_cover_and_copy_survive_both_directions(self):
        self.assertEqual(audit(evidence(), ['FgQ6IXRrk4c']), [])

    def test_hidden_or_displaced_copy_fails_on_phone_and_desktop(self):
        record = evidence()
        states = record['widths'][0]['youtube_reveals'][0]['states']
        states['playing']['copy']['h1'] = None
        states = record['widths'][-1]['youtube_reveals'][0]['states']
        states['playing']['copy']['h1'] = rect(20, 180, 200, 260)
        states['restored']['copy']['h1'] = rect(200, 300, 75, 125)
        failures = ' '.join(audit(record))
        self.assertIn('320px #hero-video, playing: release copy', failures)
        self.assertIn('1440px #hero-video: opening changes', failures)
        self.assertIn('1440px #hero-video: closing leaves', failures)

    def test_missing_player_or_unrestored_focus_fails(self):
        record = evidence()
        record['widths'][0]['youtube_reveals'] = []
        states = record['widths'][-1]['youtube_reveals'][0]['states']
        states['restored']['focus_on_opener'] = False
        failures = ' '.join(audit(record, ['FgQ6IXRrk4c']))
        self.assertIn('every detected cover', failures)
        self.assertIn('keyboard focus', failures)

    def test_expanded_frame_and_return_cannot_cover_following_section(self):
        record = evidence()
        state = record['widths'][0]['youtube_reveals'][0]['states']['playing']
        state['following'] = rect(20, 300, 180, 260)
        state['close'] = rect(120, 160, 90, 190)
        failures = ' '.join(audit(record))
        self.assertIn('following section', failures)
        self.assertIn('return control overlaps the expanded', failures)


if __name__ == '__main__':
    unittest.main()
