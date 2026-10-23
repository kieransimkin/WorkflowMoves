"""A new component or broken workflow must be visible in documentation checks."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

PACKAGE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("coverage_audit", PACKAGE/"tools/audit_workflow_coverage.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class WorkflowCoverageTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((PACKAGE/"docs/tool-workflow-map.json").read_text())

    def test_all_current_components_and_separate_toolkit(self):
        report = MODULE.validate(self.data, PACKAGE)
        self.assertEqual(report["errors"], [])
        self.assertEqual((report["component_count"], report["toolkit_count"]), (17, 1))

    def test_omitted_member_and_duplicate_are_rejected(self):
        missing = copy.deepcopy(self.data)
        missing["tools"].pop()
        self.assertFalse(MODULE.validate(missing, PACKAGE)["valid"])
        duplicate = copy.deepcopy(self.data)
        duplicate["tools"].append(duplicate["tools"][0])
        self.assertFalse(MODULE.validate(duplicate, PACKAGE)["valid"])

    def test_future_membership_cannot_silently_lose_workflow_coverage(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root/"workflows/danceflow/capabilities"
            target.mkdir(parents=True)
            shutil.copyfile(PACKAGE/"workflows/danceflow/capabilities/index.md", target/"index.md")
            with (target/"index.md").open("a") as stream:
                stream.write("\n| [Synthetic future tool](new-tool.md) | 1 | 1 | synthetic |\n")
            report = MODULE.validate(self.data, root)
            self.assertTrue(any("missing=new-tool" in error for error in report["errors"]))

    def test_missing_acceptance_or_external_workflow_path_is_rejected(self):
        for field, value in (("acceptance", []), ("workflows", ["../outside.md"]),
                             ("workflows", ["https://example.invalid/guide.md"]),
                             ("workflows", ["missing.md"]), ("workflows", ["README.md"])):
            with self.subTest(field=field, value=value):
                broken = copy.deepcopy(self.data)
                broken["tools"][0][field] = value
                self.assertFalse(MODULE.validate(broken, PACKAGE)["valid"])


if __name__ == "__main__":
    unittest.main()
