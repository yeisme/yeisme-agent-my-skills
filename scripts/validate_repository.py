#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git"}
errors: list[str] = []
names: dict[str, Path] = {}

adapter = ROOT / "scripts" / "skills.sh"
engine = ROOT / "agent-workflow" / "yeisme-skill-routing-governance" / "scripts" / "skills.sh"
if not adapter.is_file():
    errors.append("scripts/skills.sh: missing public portable manager adapter")
elif not adapter.stat().st_mode & 0o111:
    errors.append("scripts/skills.sh: public adapter must be executable")
if not engine.is_file():
    errors.append("agent-workflow management engine is missing")
elif not engine.stat().st_mode & 0o111:
    errors.append("agent-workflow management engine must be executable")

if adapter.is_file() and engine.is_file():
    adapter_help = subprocess.run(
        [str(adapter), "--help"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if adapter_help.returncode != 0 or "Portable Yeisme Skill manager" not in adapter_help.stdout:
        errors.append("scripts/skills.sh: public adapter help smoke failed")


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_PARTS for part in path.parts)


skill_files = sorted(path for path in ROOT.rglob("SKILL.md") if not is_skipped(path))
for skill_file in skill_files:
    skill_dir = skill_file.parent
    text = skill_file.read_text(encoding="utf-8")
    name_match = re.search(r"^name:\s*([^\n]+)$", text, re.MULTILINE)
    description_match = re.search(r"^description:\s*([^\n]+)$", text, re.MULTILINE)
    if not name_match:
        errors.append(f"{skill_file.relative_to(ROOT)}: missing name")
        continue
    name = name_match.group(1).strip()
    if name != skill_dir.name:
        errors.append(f"{skill_file.relative_to(ROOT)}: name must equal {skill_dir.name}")
    if name in names:
        errors.append(
            f"duplicate skill name {name}: {names[name].relative_to(ROOT)} and {skill_dir.relative_to(ROOT)}"
        )
    else:
        names[name] = skill_dir
    if not description_match or not description_match.group(1).strip():
        errors.append(f"{skill_file.relative_to(ROOT)}: missing description")
    metadata = skill_dir / "agents" / "openai.yaml"
    if not metadata.is_file():
        errors.append(f"{skill_dir.relative_to(ROOT)}: missing agents/openai.yaml")

submodule_status = subprocess.run(
    ["git", "submodule", "status", "--recursive"],
    cwd=ROOT,
    check=False,
    capture_output=True,
    text=True,
)
if submodule_status.returncode != 0:
    errors.append("git submodule status --recursive failed")
else:
    for line in submodule_status.stdout.splitlines():
        if line.startswith("-"):
            errors.append(f"uninitialized submodule: {line[1:].strip()}")
        elif line.startswith("U"):
            errors.append(f"submodule merge conflict: {line[1:].strip()}")

if errors:
    print("FAIL: repository validation failed")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print(f"PASS: validated {len(skill_files)} unique Skills and initialized submodules")
