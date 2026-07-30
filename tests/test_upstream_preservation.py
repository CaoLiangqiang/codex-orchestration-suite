from __future__ import annotations

import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
UPSTREAM_COMMIT = "37e524f590f4f2bc68845c681a38e4bacfaadf74"
INTEGRATION_MARKER = b"<!-- suite-integration:start -->\n"

UPSTREAM_HASHES = {
    "skills/team-mode/agents/openai.yaml": "c51acf2ba68eb6ed5a04ce9a7fbe3cb908aedd2f87abb5b40593a41e895bb19c",
    "skills/team-mode/references/custom-agents.md": "09d0436cbaa0e29db13238b71c648a314a2bfaf503579a62256d1a03914df2cc",
    "skills/team-mode/references/evaluation.md": "5bf72c43ed67718dff499f7a261d86c601056f6c0208b5fd42e3c44c82c19173",
    "skills/team-mode/scripts/usage_by_model.py": "d0e4f06717095eeb12f0a997722f34d0b110a054de85186f4a423d3eb0e33c19",
    "agents/Complex Executor.toml": "920bda103a9e88771cad1d0cf343030238df988199a6b9e8be34750985ab408d",
    "agents/Executor.toml": "edd19ceac4b670fada08f46384ec8436b00b4caf7680624660b00903b0ff8e18",
    "agents/Explorer.toml": "1ddbb6e4d63de24f7295fd7745a013809b573a3376eb4168f90770af64dfc717",
    "agents/Reviewer.toml": "097bb5c2c23526f387325ea30aeb68803df9f6934e16f62e36f7ea31c9c5f6f5",
    "agents/default.toml": "51216308f5201a0ec5105f476f4a2caab8d2087169f02a22bab8efc26f768f53",
}


class UpstreamPreservationTests(unittest.TestCase):
    def test_team_mode_skill_keeps_the_complete_upstream_prefix(self) -> None:
        content = (ROOT / "skills" / "team-mode" / "SKILL.md").read_bytes()
        self.assertEqual(1, content.count(INTEGRATION_MARKER))
        upstream, integration = content.split(INTEGRATION_MARKER, maxsplit=1)
        self.assertEqual(
            "7f91b071822f1a4b8694b2347739bb95523f2cffac66c956f354a214e5edfd01",
            hashlib.sha256(upstream).hexdigest(),
            f"Team Mode upstream prefix drifted from {UPSTREAM_COMMIT}",
        )
        self.assertIn(b"## Project Sessions Integration", integration)

    def test_upstream_resources_remain_byte_for_byte_identical(self) -> None:
        for relative_path, expected_hash in UPSTREAM_HASHES.items():
            with self.subTest(path=relative_path):
                content = (ROOT / relative_path).read_bytes()
                self.assertEqual(
                    expected_hash,
                    hashlib.sha256(content).hexdigest(),
                    f"{relative_path} drifted from {UPSTREAM_COMMIT}",
                )


if __name__ == "__main__":
    unittest.main()
