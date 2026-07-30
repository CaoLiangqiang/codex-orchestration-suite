from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
PROJECT_SKILL = ROOT / "skills" / "orchestrate-project-sessions"
TEAM_SKILL = ROOT / "skills" / "team-mode"


class SuiteContractTests(unittest.TestCase):
    def test_shared_contract_copies_match_canonical_source(self) -> None:
        canonical = (ROOT / "shared" / "coordination-contract.md").read_bytes()
        for skill in (PROJECT_SKILL, TEAM_SKILL):
            with self.subTest(skill=skill.name):
                self.assertEqual(canonical, (skill / "references" / "coordination-contract.md").read_bytes())

    def test_shared_contract_defines_surface_and_dispatch_gates(self) -> None:
        contract = (ROOT / "shared" / "coordination-contract.md").read_text(encoding="utf-8")
        for surface in ("Main thread", "Native subagent", "Durable Local task", "Durable Worktree task"):
            self.assertIn(surface, contract)
        for field in (
            "Outcome", "Benefit", "Context / Sources", "Scope / Ownership", "Dependencies",
            "Deliverables", "Environment", "Checks", "Stop when", "Return", "Subagent policy",
        ):
            self.assertIn(f"`{field}`", contract)
        for field in ("Unresolved risk", "Evidence", "Checks already passed", "Do not repeat"):
            self.assertIn(f"`{field}`", contract)
        self.assertIn("one writer", contract)
        self.assertIn("Reserve capacity for the controller", contract)

    def test_project_skill_requires_explicit_task_creation_authority(self) -> None:
        skill = (PROJECT_SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Task creation is authorized only when the user explicitly invokes this Skill", skill)
        self.assertIn("Treat missing policy as `disabled`", skill)
        self.assertIn("Reserve one concurrency slot for the controller", skill)
        self.assertIn("`min(4, runtime capacity minus one)`", skill)
        self.assertIn("Do not let workers create user-visible tasks", skill)
        self.assertIn("Worktree task", skill)
        self.assertIn("`$team-mode`", skill)

    def test_team_skill_cannot_escape_into_durable_or_recursive_work(self) -> None:
        skill = (TEAM_SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Team Mode never creates user-visible Codex tasks", skill)
        self.assertIn("Treat a missing `Subagent policy` as `disabled`", skill)
        self.assertIn("Durable task required:", skill)
        self.assertIn("Every native spawn must explicitly pass `agent_type`", skill)
        self.assertIn("Set every child's `Subagent policy` to `disabled`", skill)
        self.assertIn("Children must not create descendants", skill)
        for role in ("Explorer", "Executor", "Complex Executor", "Reviewer"):
            self.assertIn(f"`{role}`", skill)

    def test_skill_invocation_policies_preserve_discovery_and_authority_boundary(self) -> None:
        project_metadata = (PROJECT_SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        team_metadata = (TEAM_SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("allow_implicit_invocation: true", project_metadata)
        self.assertIn("allow_implicit_invocation: true", team_metadata)
        self.assertIn("$orchestrate-project-sessions", project_metadata)
        self.assertIn("$team-mode", team_metadata)

    def test_session_template_carries_nested_coordination_policy(self) -> None:
        template = (PROJECT_SKILL / "references" / "session-templates.md").read_text(encoding="utf-8")
        for field in ("Benefit", "Context / Sources", "Environment", "Subagent policy", "Stop when"):
            self.assertIn(f"## {field}", template)
        self.assertIn("Maximum children", template)
        self.assertIn("Child policy", template)


if __name__ == "__main__":
    unittest.main()
