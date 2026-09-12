from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---\n", 4)
    if end < 0:
        return ""
    return text[4:end]


class CaptureSkillContractTest(unittest.TestCase):
    def test_bug_skill_runs_the_script(self) -> None:
        skill = (ROOT / "skills" / "bug" / "SKILL.md").read_text(encoding="utf-8")
        meta = _frontmatter(skill)
        self.assertIn("name: bug", meta)
        self.assertIn("disable-model-invocation: true", meta)
        self.assertIn("commands/bug.mjs", skill)
        self.assertNotIn("bug-capture", skill)
        self.assertIn("Do not diagnose", skill)

    def test_patch_skill_runs_the_script(self) -> None:
        skill = (ROOT / "skills" / "patch" / "SKILL.md").read_text(encoding="utf-8")
        meta = _frontmatter(skill)
        self.assertIn("name: patch", meta)
        self.assertIn("disable-model-invocation: true", meta)
        self.assertIn("commands/patch.mjs", skill)
        self.assertIn("@fastpatch", skill)
        self.assertNotIn("bug-capture", skill)
        self.assertIn("Do not diagnose", skill)

    def test_capture_is_not_a_plugin_command(self) -> None:
        self.assertFalse((ROOT / "commands" / "bug.md").exists())
        self.assertFalse((ROOT / "commands" / "patch.md").exists())
        self.assertFalse((ROOT / "skills" / "bug-capture" / "SKILL.md").exists())
        plugin = json.loads(
            (ROOT / ".cursor-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        self.assertNotIn("commands", plugin)

    def test_agents_and_briefing_do_not_auto_route_capture(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        briefing = (ROOT / "hooks" / "synapse-briefing.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("`bug-capture`", agents)
        self.assertNotIn("bug-capture", briefing)
        self.assertNotIn("| `bug`", briefing)
        self.assertNotIn("| `patch`", briefing)
        self.assertIn("do not auto-fire", agents)


if __name__ == "__main__":
    unittest.main()
