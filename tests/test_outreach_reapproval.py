import hashlib
import importlib.util
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('reapproval_gate', Path(__file__).resolve().parents[1] / 'tools' / 'outreach_send_gate.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class ReapprovalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.old = self.root / 'old.txt'
        self.old.write_text('original approved text', encoding='utf-8')
        self.c = gate.claim(self.root, 'a@example.invalid', 'venue', 'request', 'owner', self.old, 'first approval')
        self.new = self.root / 'new.txt'
        self.new.write_text('amended approved text', encoding='utf-8')
        self.approval = self.root / 'approval.json'
        self.approval.write_text(json.dumps({'approved': True, 'packet_sha256': hashlib.sha256(self.new.read_bytes()).hexdigest()}), encoding='utf-8')
        self.evidence = self.root / 'evidence.json'
        self.evidence.write_text(json.dumps({'key': self.c['key'], 'action': self.c['action'], 'checked_at': '2026-11-02T12:00:00Z', 'send_attempted': False, 'no_sufficient_sent': True, 'fully_paginated': True, 'recipient_sent_query': 'fixture recipient', 'subject_sent_query': 'fixture subject'}), encoding='utf-8')

    def revise(self, token=None, expected=None):
        return gate.reapprove(self.root, self.c['key'], token or self.c['token'], self.new, self.approval, expected or self.c['packet_sha256'], self.evidence)

    def test_reapproval_preserves_identity_history_and_duplicate_block(self):
        original = (self.root / (self.c['action'] + '.claim.json')).read_bytes()
        revised = self.revise()
        for key in ('key', 'action', 'token', 'account', 'venue', 'obligation', 'owner'):
            self.assertEqual(revised[key], self.c[key])
        self.assertEqual(revised['revision'], 1)
        self.assertEqual(gate.inspect(self.root, self.c['key'], self.c['token']), revised)
        self.assertEqual((self.root / (self.c['action'] + '.claim.json')).read_bytes(), original)
        journal = gate.read(revised['reapproval_record'])
        self.assertEqual(journal['previous'], self.c)
        self.assertEqual(journal['current'], revised)
        receipt = self.root / 'receipt.json'
        receipt.write_text(json.dumps({'state': 'sent_verified', 'message_id': 'fixture'}), encoding='utf-8')
        self.assertEqual(gate.finish(self.root, self.c['key'], self.c['token'], receipt)['claim'], revised)
        with self.assertRaises(FileExistsError):
            gate.claim(self.root, 'a@example.invalid', 'venue', 'request', 'other', self.new, 'another approval')

    def test_wrong_owner_changed_source_stale_review_and_terminal_fail_closed(self):
        with self.assertRaises(ValueError):
            self.revise(token='not-owner')
        with self.assertRaises(ValueError):
            self.revise(expected='0' * 64)
        self.old.write_text('changed source', encoding='utf-8')
        with self.assertRaises(ValueError):
            self.revise()
        self.old.write_text('original approved text', encoding='utf-8')
        gate.write_new(self.root / (self.c['action'] + '.receipt.json'), {'state': 'sent_verified'})
        with self.assertRaises(ValueError):
            self.revise()
        self.assertEqual(gate.inspect(self.root, self.c['key'], self.c['token']), self.c)

    def test_exact_approval_and_full_unsent_evidence_required(self):
        original_evidence = gate.read(self.evidence)
        for field, bad in [('send_attempted', True), ('no_sufficient_sent', False), ('fully_paginated', False), ('key', 'wrong'), ('action', 'wrong'), ('recipient_sent_query', ''), ('subject_sent_query', '')]:
            self.evidence.write_text(json.dumps(dict(original_evidence, **{field: bad})), encoding='utf-8')
            with self.assertRaises(ValueError):
                self.revise()
        self.evidence.write_text(json.dumps(original_evidence), encoding='utf-8')
        self.new.write_text('unapproved change', encoding='utf-8')
        with self.assertRaises(ValueError):
            self.revise()
        self.assertEqual(gate.inspect(self.root, self.c['key'], self.c['token']), self.c)

    def test_competing_reapprovals_have_one_winner(self):
        def attempt(_):
            try:
                return self.revise()
            except (ValueError, FileExistsError):
                return None
        with ThreadPoolExecutor(max_workers=8) as pool:
            outcomes = list(pool.map(attempt, range(16)))
        self.assertEqual(sum(x is not None for x in outcomes), 1)
        self.assertEqual(len(list(self.root.glob('*.reapproval.*.json'))), 1)
        self.assertFalse(list(self.root.glob('*.transition.json')))

    def test_transition_and_replace_failure_never_rebind_or_delete_claim(self):
        transition = self.root / (self.c['key'] + '.transition.json')
        gate.write_new(transition, {'nonce': 'fixture pending transition'})
        with self.assertRaises(ValueError):
            gate.inspect(self.root, self.c['key'], self.c['token'])
        with self.assertRaises(FileExistsError):
            self.revise()
        transition.unlink()
        with patch.object(gate.os, 'replace', side_effect=OSError('fixture atomic replace failure')):
            with self.assertRaises(OSError):
                self.revise()
        self.assertEqual(gate.inspect(self.root, self.c['key'], self.c['token']), self.c)
        self.assertTrue((self.root / (self.c['action'] + '.claim.json')).exists())
        self.assertEqual(len(list(self.root.glob('*.reapproval.*.json'))), 1)
        self.assertFalse(list(self.root.glob('*.tmp')))


if __name__ == '__main__':
    unittest.main()
