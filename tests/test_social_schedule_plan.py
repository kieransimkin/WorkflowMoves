import copy
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('social_plan', Path(__file__).parents[1] / 'tools/social_schedule_plan.py')
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)
NOW = datetime(2026, 10, 23, tzinfo=timezone.utc)


class SocialPlanTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ('video', 'caption', 'evidence'):
            (self.root / name).write_text('synthetic ' + name, encoding='utf-8')
        self.row = dict(id='one', destination='example', account='synthetic', state='prepared',
                        local_time='2026-11-27T18:00:00', timezone='Europe/London', utc='2026-11-27T18:00:00Z',
                        files={n: {'path': n, 'sha256': M.digest((self.root / n).read_bytes())} for n in ('video', 'caption')},
                        settings={'visibility': 'public_future'}, queue_check={'observed_at': NOW.isoformat(), 'evidence': 'evidence'})
        self.approve(self.row)

    def approve(self, row):
        row['approval'] = {'payload_sha256': M.payload_hash(row), 'evidence': 'evidence'}

    def check(self, *rows):
        return M.evaluate({'schema': 'workflowmoves.social-plan.v1', 'items': list(rows or [self.row])}, self.root, NOW)

    def test_prepared_is_only_ready_for_fresh_native_preflight(self):
        result = self.check()
        self.assertTrue(result['valid'])
        self.assertEqual(result['items'][0]['action'], 'ready_for_native_preflight')
        self.assertEqual(self.row['state'], 'prepared')

    def test_approval_is_invalidated_by_slot_or_settings_change(self):
        self.row['settings']['visibility'] = 'private'
        self.assertIn('approval', self.check()['items'][0]['holds'][0])

    def test_changed_file_bytes_fail(self):
        (self.root / 'video').write_text('different')
        self.assertFalse(self.check()['valid'])

    def test_daylight_saving_gap_rejected_and_fold_explicit(self):
        with self.assertRaises(ValueError):
            M.resolve_time('2027-03-28T01:30:00', 'Europe/London', '2027-03-28T01:30:00Z')
        for utc in ('2026-10-25T00:30:00Z', '2026-10-25T01:30:00Z'):
            self.assertEqual(M.resolve_time('2026-10-25T01:30:00', 'Europe/London', utc).hour, int(utc[11:13]))

    def test_pending_external_job_blocks_takeover(self):
        self.row['replaces'] = [{'state': 'pending', 'evidence': 'evidence'}]
        self.assertIn('cancellation', self.check()['items'][0]['holds'][0])
        self.row['replaces'][0]['state'] = 'cancelled_verified'
        self.assertEqual(self.check()['items'][0]['action'], 'ready_for_native_preflight')

    def test_pending_mutation_and_window_do_not_create_retry(self):
        self.row.update(state='mutation_pending', window={'last_selectable_date': '2026-11-21', 'next_check': '2026-10-29'})
        item = self.check()['items'][0]
        self.assertEqual(item['action'], 'hold')
        self.assertEqual(item['next_action_at'], '2026-10-29')
        self.assertTrue(any('do not resubmit' in h for h in item['holds']))
        self.assertFalse(any('existing private draft' in h for h in item['holds']))
        self.row['state'] = 'private_draft'
        self.assertTrue(any('existing private draft' in h for h in self.check()['items'][0]['holds']))

    def test_same_asset_and_same_slot_conflicts(self):
        second = copy.deepcopy(self.row)
        second['id'] = 'two'
        self.assertFalse(self.check(self.row, second)['valid'])
        second['files']['video']['sha256'] = '0' * 64
        self.approve(second)
        problems = self.check(self.row, second)['items'][1]['problems']
        self.assertTrue(any('Slot collision' in p for p in problems))

    def test_native_receipt_required_and_checked(self):
        self.row['state'] = 'scheduled'
        self.assertFalse(self.check()['valid'])
        self.row['native_receipt'] = {'id_or_url': 'synthetic-id', 'utc': self.row['utc'], 'evidence': 'evidence'}
        self.assertEqual(self.check()['items'][0]['action'], 'already_persisted')

    def test_html_escapes_untrusted_account_text(self):
        self.row['account'] = '<script>evil()</script>'
        html = M.render_html(self.check())
        self.assertNotIn('<script>', html)
        self.assertIn('&lt;script&gt;', html)


if __name__ == '__main__':
    unittest.main()
