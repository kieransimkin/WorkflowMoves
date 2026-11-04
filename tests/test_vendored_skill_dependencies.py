import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("vendor_audit", ROOT / "tools" / "audit_vendored_skill_dependencies.py")
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class VendoredSkillDependenciesTests(unittest.TestCase):
    def test_snapshot_hashes_licences_and_blockers(self):
        rows = AUDIT.audit(ROOT)
        states = {row["id"]: row["status"] for row in rows}
        self.assertEqual(states["skill-creator"], "vendored")
        self.assertEqual(states["browser:control-in-app-browser"], "blocked_proprietary")
        self.assertEqual(states["review-agent"], "blocked_no_redistribution_license")

    def test_changed_vendored_file_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            shutil.copy2(ROOT / "external-skill-dependencies.json", root / "external-skill-dependencies.json")
            source = ROOT / "vendor" / "skill-dependencies"
            target = root / "vendor" / "skill-dependencies"
            shutil.copytree(source, target)
            skill = target / "codex-system" / "skill-creator" / "SKILL.md"
            skill.write_bytes(skill.read_bytes() + b"\nchanged\n")
            with self.assertRaisesRegex(ValueError, "Vendored dependency mismatch"):
                AUDIT.audit(root)

    def test_every_vendored_skill_has_skill_file_and_associated_content(self):
        manifest = json.loads((ROOT / "external-skill-dependencies.json").read_text(encoding="utf-8"))
        for row in manifest["dependencies"]:
            if row["copy_status"] != "vendored":
                continue
            path = ROOT / row["vendored_path"]
            self.assertTrue((path / "SKILL.md").is_file())
            self.assertGreater(len([item for item in path.rglob("*") if item.is_file()]), 1)


if __name__ == "__main__":
    unittest.main()
