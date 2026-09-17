#!/usr/bin/env python3
"""Validate the additive creative Grilling skill matrix without model calls."""

from pathlib import Path
import re
import sys


SKILL_DIR = Path(__file__).resolve().parents[1]
MODULE_ROOT = SKILL_DIR.parent
# Runtime copies live under .claude/skills or .agents/skills while the
# publishable source and the narrow handoff skills live under the workspace
# .skills tree, so resolve the workspace root by marker, not fixed parent hops.
WORKSPACE_ROOT = next(
    (parent for parent in SKILL_DIR.parents if (parent / ".skills" / "profiles").is_dir()),
    None,
)
if WORKSPACE_ROOT is None:
    print("ERROR: cannot locate workspace root (.skills/profiles)", file=sys.stderr)
    raise SystemExit(1)
YEISME_ROOT = WORKSPACE_ROOT / ".skills" / "yeisme"

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

# Narrow handoff skills load on demand via skillctl per the maintained root
# profile policy (see the policy comment inside .skills/profiles files), so
# targets/cli/auctra.txt only pins the resident interview entries.
PROFILE_EXPECTATIONS = {
    "root.txt": {"creative-grilling", "creative-grill-me", "novel-grill-me", "manga-drama-grill-me"},
    "targets/cli/auctra.txt": {"creative-grilling", "novel-grill-me"},
    "targets/agent/scaena.txt": {"creative-grilling", "manga-drama-grill-me", "scaena-production-decision-handoff"},
    "targets/data/screenwriting-media-creation.txt": {"creative-grilling", "manga-drama-grill-me"},
}

CASE_IDS = {f"CG-{index:02d}" for index in range(1, 27)}
SCHEMAS = {
    "creative.grill-route.v0.1",
    "creative.decision-brief.v0.1",
    "creative.owner-handoff.v0.1",
    "creative.owner-session-binding.v0.1",
}

BINDING_FIELDS = (
    "binding_version",
    "owner_capability_ref",
    "session_revision",
    "session_digest",
    "source_refs",
    "workflow_version",
    "action_id",
    "input_schema_ref",
    "expected_revision",
    "permission",
)

CANARY_IDS = tuple(f"CAN-{index:02d}" for index in range(1, 9))


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

binding_section = contracts.split("creative.owner-session-binding.v0.1", 1)
if len(binding_section) < 2:
    fail("contracts.md must define creative.owner-session-binding.v0.1")
binding_body = binding_section[1]
for field in BINDING_FIELDS:
    if field not in binding_body:
        fail(f"owner-session binding is missing field {field}")
for guard in ("不执行", "shell"):
    if guard not in binding_body:
        fail(f"owner-session binding must keep the shell-template guard ({guard})")

frontier = (SKILL_DIR / "references" / "frontier-protocol.md").read_text(encoding="utf-8")
for token in ("恢复", "刷新", "重开", "needs_refresh", "稳定 ref"):
    if token not in frontier:
        fail(f"frontier-protocol.md must cover recovery token {token}")

canaries = (SKILL_DIR / "references" / "canaries.md").read_text(encoding="utf-8")
for canary in CANARY_IDS:
    if f"## {canary}" not in canaries:
        fail(f"canaries.md is missing {canary}")
if canaries.count("结论：通过") < len(CANARY_IDS):
    fail("canaries.md must record a conclusion for every canary")

writer = (SKILL_DIR / "references" / "writer-handoff.md").read_text(encoding="utf-8")
for token in ("不写正文", "不自动 accept", "reject-all", "维持基线", "F1", "F2", "F3", "不跨项目"):
    if token not in writer:
        fail(f"writer-handoff.md must cover {token}")

host = (SKILL_DIR / "references" / "host-adaptation.md").read_text(encoding="utf-8")
for token in ("needs_contract", "编号文本", "chat-only"):
    if token not in host:
        fail(f"host-adaptation.md must cover {token}")

decision_map = (SKILL_DIR / "references" / "ai-drama-decision-map.md").read_text(encoding="utf-8")
for token in ("短剧", "电视", "电影", "单元", "喜剧", "音频", "零路由追问", "ai-drama-router"):
    if token not in decision_map:
        fail(f"ai-drama-decision-map.md must cover {token}")

novel_frontiers = (
    MODULE_ROOT / "novel-grill-me" / "references" / "novel-frontiers.md"
).read_text(encoding="utf-8")
for token in ("想法", "人物", "结构", "章节", "场景", "成稿", "修订", "中途进入"):
    if token not in novel_frontiers:
        fail(f"novel-frontiers.md must cover stage {token}")

manga_frontiers = (
    MODULE_ROOT / "manga-drama-grill-me" / "references" / "manga-drama-frontiers.md"
).read_text(encoding="utf-8")
for token in ("阶段进入", "proof", "中途进入"):
    if token not in manga_frontiers:
        fail(f"manga-drama-frontiers.md must cover {token}")

profiles_root = WORKSPACE_ROOT / ".skills" / "profiles"
for relative, expected in PROFILE_EXPECTATIONS.items():
    path = profiles_root / relative
    if not path.is_file():
        fail(f"missing profile {relative}")
    missing = expected - profile_entries(path)
    if missing:
        fail(f"profile {relative} is missing {sorted(missing)}")

print("creative grilling matrix is valid")
