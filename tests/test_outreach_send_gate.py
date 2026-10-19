import importlib.util
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('send_gate', Path(__file__).resolve().parents[1] / 'tools' / 'outreach_send_gate.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

class SendGateTests(unittest.TestCase):
    def test_verified_form_receipt_has_no_invented_message_id(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as d:
            root = Path(d)
            packet = root / 'packet.txt'
            packet.write_text('approved form fixture', encoding='utf-8')
            c = gate.claim(root, 'a@example.invalid', 'form-venue', 'original-request', 'owner', packet, 'fixture approval')
            evidence = root / 'visible-success.txt'
            evidence.write_text('Your submission was successful.', encoding='utf-8')
            receipt = root / 'receipt.json'
            value = {'state': 'submission_verified', 'destination_url': 'https://example.invalid/form',
                     'success_observed': 'Your submission was successful.',
                     'evidence_files': [{'path': str(evidence), 'sha256': hashlib.sha256(evidence.read_bytes()).hexdigest()}]}
            receipt.write_text(json.dumps(value), encoding='utf-8')
            result = gate.finish(root, c['key'], c['token'], receipt)
            self.assertNotIn('message_id', result['evidence'])
            self.assertFalse(list(root.glob('*.active.json')))
            with self.assertRaises(FileExistsError):
                gate.claim(root, 'a@example.invalid', 'form-venue', 'original-request', 'other', packet, 'fixture')

    def test_unverified_form_evidence_retains_claim(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as d:
            root = Path(d)
            packet = root / 'packet.txt'
            packet.write_text('approved', encoding='utf-8')
            c = gate.claim(root, 'a@example.invalid', 'form-venue', 'request', 'owner', packet, 'fixture')
            evidence = root / 'success.txt'
            evidence.write_text('fixture', encoding='utf-8')
            receipt = root / 'receipt.json'
            base = {'state': 'submission_verified', 'destination_url': 'https://example.invalid/form',
                    'success_observed': 'Success', 'evidence_files': [{'path': str(evidence), 'sha256': hashlib.sha256(evidence.read_bytes()).hexdigest()}]}
            for bad in ({**base, 'success_observed': ''}, {**base, 'evidence_files': []},
                        {**base, 'evidence_files': [{'path': str(evidence), 'sha256': '0' * 64}]}):
                receipt.write_text(json.dumps(bad), encoding='utf-8')
                with self.assertRaises(ValueError):
                    gate.finish(root, c['key'], c['token'], receipt)
                self.assertTrue((root / (c['key'] + '.active.json')).exists())
            self.assertFalse(list(root.glob('*.receipt.json')))

    def test_competing_owners_and_permanent_duplicate_block(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as d:
            root = Path(d)
            packet = root / 'packet.txt'
            packet.write_text('exact approved fixture', encoding='utf-8')
            def attempt(owner):
                try:
                    return gate.claim(root, 'a@example.invalid', 'venue', 'request', owner, packet, 'fixture approval')
                except FileExistsError:
                    return None
            with ThreadPoolExecutor(max_workers=8) as pool:
                results = list(pool.map(attempt, [str(i) for i in range(16)]))
            wins = [x for x in results if x]
            self.assertEqual(len(wins), 1)
            win = wins[0]
            with self.assertRaises(ValueError):
                gate.inspect(root, win['key'], 'wrong-owner')
            receipt = root / 'receipt.json'
            receipt.write_text(json.dumps({'state':'sent_verified','message_id':'fixture-only'}), encoding='utf-8')
            gate.finish(root, win['key'], win['token'], receipt)
            with self.assertRaises(FileExistsError):
                gate.claim(root, 'a@example.invalid', 'venue', 'request', 'other', packet, 'fixture')
            self.assertFalse(list(root.glob('*.active.json')))
            self.assertEqual(len(list(root.glob('*.receipt.json'))), 1)

    def test_changed_packet_and_uncertain_state_fail_closed(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as d:
            root = Path(d)
            packet = root / 'packet.txt'
            packet.write_text('approved', encoding='utf-8')
            c = gate.claim(root,'a@example.invalid','venue','request','owner',packet,'fixture')
            packet.write_text('changed', encoding='utf-8')
            with self.assertRaises(ValueError):
                gate.inspect(root,c['key'],c['token'])
            packet.write_text('approved', encoding='utf-8')
            receipt = root / 'receipt.json'
            receipt.write_text('{"state":"uncertain"}', encoding='utf-8')
            with self.assertRaises(ValueError):
                gate.finish(root,c['key'],c['token'],receipt)
            self.assertEqual(len(list(root.glob('*.active.json'))),1)

if __name__ == '__main__':
    unittest.main()
