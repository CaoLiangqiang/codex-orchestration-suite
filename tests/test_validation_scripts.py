from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


def load_script(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sync_resources = load_script("sync_suite_resources", ROOT / "scripts" / "sync_suite_resources.py")
validate_skills = load_script("validate_skills", ROOT / "scripts" / "validate_skills.py")


class ValidationScriptTests(unittest.TestCase):
    def test_suite_skills_pass_portable_validator(self) -> None:
        for name in ("orchestrate-project-sessions", "team-mode"):
            with self.subTest(name=name):
                self.assertEqual(validate_skills.validate_skill(ROOT / "skills" / name), [])

    def test_skill_validator_rejects_directory_name_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "wrong-name"
            (skill / "agents").mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: expected-name\ndescription: Complete test description.\n---\n\n# Test\n",
                encoding="utf-8",
            )
            (skill / "agents" / "openai.yaml").write_text(
                'interface:\n  display_name: "Test"\n  short_description: "A sufficiently long test description"\n'
                '  default_prompt: "Use $expected-name for this test."\n\npolicy:\n'
                "  allow_implicit_invocation: true\n",
                encoding="utf-8",
            )
            errors = validate_skills.validate_skill(skill)
            self.assertTrue(any("must match directory" in error for error in errors))

    def test_sync_check_detects_unexpected_bundled_profile(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Explorer.toml").write_text("name = 'Explorer'\n", encoding="utf-8")
            (root / "obsolete.toml").write_text("name = 'obsolete'\n", encoding="utf-8")
            unexpected = sync_resources.unexpected_files(root, {"Explorer.toml"})
            self.assertEqual([path.name for path in unexpected], ["obsolete.toml"])


if __name__ == "__main__":
    unittest.main()
