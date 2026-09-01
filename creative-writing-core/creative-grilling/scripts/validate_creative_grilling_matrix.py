#!/usr/bin/env python3
"""Validate the additive creative Grilling skill matrix without model calls."""

from pathlib import Path
import re
import sys


SKILL_DIR = Path(__file__).resolve().parents[1]
MODULE_ROOT = SKILL_DIR.parent
YEISME_ROOT = MODULE_ROOT.parent
WORKSPACE_ROOT = YEISME_ROOT.parents[1]

SKILLS = {
    "creative-grilling": MODULE_ROOT / "creative-grilling",
    "creative-grill-me": MODULE_ROOT / "creative-grill-me",
    "novel-grill-me": MODULE_ROOT / "novel-grill-me",
    "manga-drama-grill-me": MODULE_ROOT / "manga-drama-grill-me",
    "auctra-creative-decision-handoff": YEISME_ROOT
    / "auctra-novel"
    / "auctra-runtime"
    / "auctra-creative-decision-handoff",
    "scaena-production-decision-handoff": YEISME_ROOT
    / "scaena"
    / "scaena-production-decision-handoff",
}

PROFILE_EXPECTATIONS = {
    "root.txt": {"creative-grilling", "creative-grill-me", "novel-grill-me", "manga-drama-grill-me"},
    "targets/cli/auctra.txt": {"creative-grilling", "novel-grill-me", "auctra-creative-decision-handoff"},
    "targets/agent/scaena.txt": {"creative-grilling", "manga-drama-grill-me", "scaena-production-decision-handoff"},
    "targets/data/screenwriting-media-creation.txt": {"creative-grilling", "manga-drama-grill-me"},
}

CASE_IDS = {f"CG-{index:02d}" for index in range(1, 15)}
SCHEMAS = {
    "creative.grill-route.v0.1",
    "creative.decision-brief.v0.1",
    "creative.owner-handoff.v0.1",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def profile_entries(path: Path) -> set[str]:
    return {
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


for name, path in SKILLS.items():
    skill = path / "SKILL.md"
    metadata = path / "agents" / "openai.yaml"
    if not skill.is_file() or not metadata.is_file():
        fail(f"{name} must contain SKILL.md and agents/openai.yaml")
    body = skill.read_text(encoding="utf-8")
    match = re.search(r"^name:\s*([^\n]+)$", body, re.MULTILINE)
    if not match or match.group(1).strip() != name:
        fail(f"{name} frontmatter name mismatch")

for entry in ("creative-grill-me", "novel-grill-me", "manga-drama-grill-me"):
    metadata = (SKILLS[entry] / "agents" / "openai.yaml").read_text(encoding="utf-8")
    if "allow_implicit_invocation: false" not in metadata:
        fail(f"{entry} must be explicit-only")

matrix = (SKILL_DIR / "references" / "route-matrix.md").read_text(encoding="utf-8")
found_cases = set(re.findall(r"CASE (CG-\d{2})", matrix))
if found_cases != CASE_IDS:
    fail(f"route matrix cases mismatch: expected {sorted(CASE_IDS)}, got {sorted(found_cases)}")

contracts = (SKILL_DIR / "references" / "contracts.md").read_text(encoding="utf-8")
for schema in SCHEMAS:
    if schema not in contracts:
        fail(f"missing contract {schema}")

profiles_root = WORKSPACE_ROOT / ".skills" / "profiles"
for relative, expected in PROFILE_EXPECTATIONS.items():
    path = profiles_root / relative
    if not path.is_file():
        fail(f"missing profile {relative}")
    missing = expected - profile_entries(path)
    if missing:
        fail(f"profile {relative} is missing {sorted(missing)}")

print("creative grilling matrix is valid")
