#!/usr/bin/env python3
"""Regression test for the curl-friendly Yeisme network installer."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install.sh"
AGENT_WORKFLOW = ROOT / "agent-workflow"


def write_skill(root: Path, name: str) -> None:
    skill = root / name
    (skill / "agents").mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: Use when testing {name}.\n---\n\n# {name}\n",
        encoding="utf-8",
    )
    (skill / "agents" / "openai.yaml").write_text(
        f'display_name: "{name}"\n'
        f'short_description: "Test {name}."\n'
        f'default_prompt: "Use ${name}."\n',
        encoding="utf-8",
    )


class NetworkInstallTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.source_repo = self.base / "source-repo"
        self.checkout = self.base / "checkout"
        self.project = self.base / "project"
        (self.source_repo / "scripts").mkdir(parents=True)
        self.project.mkdir()

        shutil.copy2(ROOT / "scripts" / "skills.sh", self.source_repo / "scripts" / "skills.sh")
        manager_target = self.source_repo / "agent-workflow" / "yeisme-skill-routing-governance"
        builder_target = self.source_repo / "agent-workflow" / "yeisme-builder-profile"
        shutil.copytree(AGENT_WORKFLOW / "yeisme-skill-routing-governance", manager_target)
        shutil.copytree(AGENT_WORKFLOW / "yeisme-builder-profile", builder_target)
        write_skill(self.source_repo, "ai-drama-router")

        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.source_repo, check=True)
        subprocess.run(["git", "config", "user.name", "Yeisme Test"], cwd=self.source_repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=self.source_repo, check=True)
        subprocess.run(["git", "add", "."], cwd=self.source_repo, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "test source"], cwd=self.source_repo, check=True)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_installer(self, mode: str, *skills: str) -> subprocess.CompletedProcess[str]:
        skill_args: list[str] = []
        for skill in skills:
            skill_args.extend(["--skill", skill])
        return subprocess.run(
            [
                str(INSTALLER),
                "--repo",
                str(self.source_repo),
                "--ref",
                "main",
                "--source-dir",
                str(self.checkout),
                "--project",
                str(self.project),
                *skill_args,
                mode,
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_json_and_agent_install_are_idempotent(self) -> None:
        first = self.run_installer("--json", "ai-drama-router")
        self.assertEqual(first.returncode, 0, first.stderr)
        envelope = json.loads(first.stdout)
        self.assertEqual(envelope["spec_version"], "1.0")
        self.assertEqual(envelope["mode"], "json")
        self.assertEqual(envelope["command"], "skills.network-install")
        self.assertEqual(envelope["status"], "success")
        self.assertEqual(envelope["facts"]["builder_profile"], "none")
        self.assertEqual(envelope["data"]["skills"], ["ai-drama-router"])

        profile = self.project / ".skills" / "profiles" / "root.txt"
        profile_text = profile.read_text(encoding="utf-8")
        for skill in ("yeisme-skill-routing-governance", "ai-drama-router"):
            self.assertIn(skill, profile_text)
            for home in (".agents", ".claude"):
                self.assertTrue((self.project / home / "skills" / skill / "SKILL.md").is_file())
        self.assertNotIn("yeisme-builder-profile", profile_text)
        for home in (".agents", ".claude"):
            self.assertFalse((self.project / home / "skills" / "yeisme-builder-profile").exists())
        self.assertNotIn("project-development-router", profile_text)

        second = self.run_installer(
            "--agent", "yeisme-builder-profile", "ai-drama-router"
        )
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("spec_version=1.0", second.stdout)
        self.assertIn("mode=agent", second.stdout)
        self.assertIn("command=skills.network-install", second.stdout)
        self.assertIn("status=success", second.stdout)
        self.assertIn("fact.builder_profile=yeisme-builder-profile", second.stdout)
        self.assertIn("item.skill.1=yeisme-builder-profile", second.stdout)
        self.assertIn("item.skill.2=ai-drama-router", second.stdout)

        profile_text = profile.read_text(encoding="utf-8")
        self.assertIn("yeisme-builder-profile", profile_text)
        for home in (".agents", ".claude"):
            self.assertTrue(
                (self.project / home / "skills" / "yeisme-builder-profile" / "SKILL.md").is_file()
            )


if __name__ == "__main__":
    unittest.main()
