import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("hashtag_social_plan", Path(__file__).parents[1] / "tools/social_schedule_plan.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)
NOW = datetime(2026, 10, 24, tzinfo=timezone.utc)


class AuditCompositionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ("video", "caption", "evidence"):
            (self.root / name).write_text("synthetic " + name, encoding="utf-8")
        self.audit = {"plugin": "hashtag-planner", "operation": "audit", "metadata": {
            "passed": True, "issues": [], "target_platform": "youtube",
            "asset_sha256": M.digest((self.root / "video").read_bytes()),
            "caption_sha256": M.digest((self.root / "caption").read_bytes()),
            "checked_at": NOW.isoformat(), "reviewed_at": NOW.isoformat(), "native_checked_at": NOW.isoformat()}}
        self.row = dict(id="one", destination="youtube", account="synthetic", state="prepared",
            local_time="2026-11-27T18:00:00", timezone="Europe/London", utc="2026-11-27T18:00:00Z",
            files={n: {"path": n, "sha256": M.digest((self.root / n).read_bytes())} for n in ("video", "caption")},
            settings={"require_hashtag_review": True}, queue_check={"observed_at": NOW.isoformat(), "evidence": "evidence"})
        self.save()

    def save(self):
        p = self.root / "audit.json"
        p.write_text(json.dumps(self.audit), encoding="utf-8")
        self.row["hashtag_audit"] = {"path": "audit.json", "sha256": M.digest(p.read_bytes())}
        self.row["approval"] = {"payload_sha256": M.payload_hash(self.row), "evidence": "evidence"}

    def check(self):
        return M.evaluate({"schema": "workflowmoves.social-plan.v1", "items": [self.row]}, self.root, NOW)["items"][0]

    def test_fresh_exact_receipt_allows_future_native_preflight(self):
        self.assertEqual(self.check()["action"], "ready_for_native_preflight")

    def test_missing_required_receipt_holds(self):
        del self.row["hashtag_audit"]
        self.assertTrue(any("audit required" in h for h in self.check()["holds"]))

    def test_changed_receipt_and_nonpassing_claim_hold(self):
        (self.root / "audit.json").write_text("{}")
        self.assertTrue(any("changed receipt" in h for h in self.check()["holds"]))
        self.audit["metadata"]["passed"] = "true"
        self.save()
        self.assertTrue(any("not a passing" in h for h in self.check()["holds"]))

    def test_platform_asset_and_caption_mismatch_hold(self):
        for field in ("target_platform", "asset_sha256", "caption_sha256"):
            old = self.audit["metadata"][field]
            self.audit["metadata"][field] = "wrong"
            self.save()
            self.assertTrue(any("Hashtag audit hold" in h for h in self.check()["holds"]))
            self.audit["metadata"][field] = old

    def test_expired_or_future_check_holds(self):
        for field, value in (("native_checked_at", "2026-09-01T00:00:00Z"), ("checked_at", "2027-01-01T00:00:00Z")):
            old = self.audit["metadata"][field]
            self.audit["metadata"][field] = value
            self.save()
            self.assertTrue(any("Hashtag audit hold" in h for h in self.check()["holds"]))
            self.audit["metadata"][field] = old

    def test_receipt_is_in_exact_payload_approval(self):
        old = M.payload_hash(self.row)
        self.row["hashtag_audit"]["sha256"] = "0" * 64
        self.assertNotEqual(M.payload_hash(self.row), old)

    def test_legacy_without_opt_in_is_unchanged(self):
        del self.row["hashtag_audit"]
        self.row["settings"] = {}
        self.row["approval"] = {"payload_sha256": M.payload_hash(self.row), "evidence": "evidence"}
        self.assertEqual(self.check()["action"], "ready_for_native_preflight")
