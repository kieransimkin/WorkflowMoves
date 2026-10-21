import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location("check_blogworthiness", Path(__file__).resolve().parents[1] / "tools/check_blogworthiness.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class BlogworthinessTests(unittest.TestCase):
    def base(self):
        return {"task": "Synthetic demonstration", "decision": "PASS", "reason": "Useful experiment",
                "evidence": ["synthetic-evidence.json"], "angle": "What changed", "duplicate_check": "Current posts and drafts checked",
                "next_action": "Prepare article", "state": "prepared"}

    def test_fail_retains_reason_and_evidence(self):
        self.assertEqual(MODULE.validate({"task": "Routine cleanup", "decision": "FAIL", "reason": "Administration only", "evidence": ["record.md"]}), [])
        self.assertTrue(MODULE.validate({"task": "Cleanup", "decision": "FAIL", "reason": ""}))

    def test_blocked_pass_is_valid_without_pretending_to_publish(self):
        row = self.base()
        row.update(state="blocked", blocker="No authorised public screenshot")
        self.assertEqual(MODULE.validate(row), [])
        del row["blocker"]
        self.assertTrue(MODULE.validate(row))

    def test_passing_story_requires_duplicate_review_and_delivery(self):
        row = self.base()
        self.assertEqual(MODULE.validate(row), [])
        for key in ("angle", "evidence", "duplicate_check", "next_action", "state"):
            broken = dict(row)
            del broken[key]
            self.assertTrue(MODULE.validate(broken), key)

    def test_public_state_requires_receipt_url(self):
        row = self.base()
        row["state"] = "verified_live"
        self.assertTrue(MODULE.validate(row))
        row["url"] = "https://example.invalid/synthetic-article/"
        self.assertEqual(MODULE.validate(row), [])

    def test_unknown_decisions_and_nonobjects_fail(self):
        row = self.base()
        row["decision"] = "SKIPPED"
        self.assertTrue(MODULE.validate(row))
        self.assertTrue(MODULE.validate("PASS"))
