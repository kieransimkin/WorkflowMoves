from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RenderOwnershipPolicy(unittest.TestCase):
    def test_workflow_uses_full_length_or_over_fifteen_minutes(self):
        text = (ROOT / "workflows" / "framerudiments-rendering.md").read_text(encoding="utf-8")
        self.assertIn("full-length video", text)
        self.assertIn("more than 15 minutes", text)
        self.assertIn("Keep every other\nrender inside the active Codex session", text)
        self.assertIn("render-progress.json", text)
        self.assertIn("do not recursively scan frame, chunk or QA directories", text)
        self.assertNotIn("Every long-running or high-quality render", text)

    def test_skill_fragment_and_scheduled_guide_match_threshold(self):
        fragment = (ROOT / "fragments" / "framerudiments-rendering.md").read_text(encoding="utf-8")
        scheduled = (ROOT / "workflows" / "scheduled-danceflow-tool-use.md").read_text(
            encoding="utf-8"
        )
        for text in (fragment, scheduled):
            self.assertIn("full-length video", text)
            self.assertIn("15 minutes", text)
            self.assertIn("render-progress.json", text)


if __name__ == "__main__":
    unittest.main()
