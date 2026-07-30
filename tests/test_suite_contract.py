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
        self.assertIn("Creating tasks is authorized only when the user explicitly invokes this skill", skill)
        self.assertIn("Treat a missing policy as `disabled`", skill)
        self.assertIn("Leave one concurrency slot available for the controller", skill)
        self.assertIn("Dispatch no more than four workers at once", skill)
        self.assertIn("Do not let worker tasks create more user-owned tasks", skill)
        self.assertIn("Use a Git Worktree for concurrent code-writing tasks", skill)
        self.assertIn("`$team-mode`", skill)

    def test_suite_limits_homogeneous_read_only_fanout(self) -> None:
        contract = (ROOT / "shared" / "coordination-contract.md").read_text(encoding="utf-8")
        project_skill = (PROJECT_SKILL / "SKILL.md").read_text(encoding="utf-8")

        for content in (contract, project_skill):
            self.assertIn("several small, homogeneous sources", content)
            self.assertIn("one Explorer", content)
            self.assertIn("independent evidence slice", content)
            self.assertIn("coordination cost", content)

    def test_team_skill_cannot_escape_into_durable_or_recursive_work(self) -> None:
        skill = (TEAM_SKILL / "SKILL.md").read_text(encoding="utf-8")
        integration = (TEAM_SKILL / "references" / "project-sessions-integration.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("standalone Team Mode behavior above remains unchanged", skill)
        self.assertIn("Team Mode never creates user-visible tasks", integration)
        self.assertIn("policy is missing, treat it as `disabled`", integration)
        self.assertIn("Durable task required:", skill)
        self.assertIn("Every `spawn_agent` call must explicitly pass `agent_type`", skill)
        self.assertIn("Every child brief must set its own `Subagent policy` to `disabled`", integration)
        self.assertIn("children never spawn descendants", skill)
        for role in ("Explorer", "Executor", "Complex Executor", "Reviewer"):
            self.assertIn(f"`{role}`", integration)

    def test_skill_invocation_policies_preserve_discovery_and_authority_boundary(self) -> None:
        project_metadata = (PROJECT_SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        team_metadata = (TEAM_SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("allow_implicit_invocation: true", project_metadata)
        self.assertIn("allow_implicit_invocation: true", team_metadata)
        self.assertIn("$orchestrate-project-sessions", project_metadata)
        self.assertIn("$team-mode", team_metadata)

    def test_session_template_carries_nested_coordination_policy(self) -> None:
        template = (PROJECT_SKILL / "references" / "session-templates.md").read_text(encoding="utf-8")
        for field in ("Benefit", "Context", "Sources", "Environment", "Subagent policy", "Stop when"):
            self.assertIn(f"## {field}", template)
        self.assertIn("Maximum children", template)
        self.assertIn("Child policy", template)

    def test_project_skill_retains_original_controller_workflow(self) -> None:
        skill = (PROJECT_SKILL / "SKILL.md").read_text(encoding="utf-8")
        for heading in (
            "## Operating model",
            "## Phase 1: Ground the controller",
            "## Phase 2: Build the task graph",
            "## Phase 3: Choose task and workspace type",
            "## Phase 4: Dispatch",
            "## Phase 5: Monitor and steer",
            "## Phase 6: Verify worker results",
            "## Phase 7: Integrate and close",
            "## Fallbacks and boundaries",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, skill)
        self.assertIn("Use Handoff when a completed or blocked Worktree task needs to continue in Local", skill)
        self.assertIn("Reuse returned cursors", skill)
        self.assertIn("Do not start OMX Team automatically", skill)


if __name__ == "__main__":
    unittest.main()
