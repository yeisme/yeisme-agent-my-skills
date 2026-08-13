#!/usr/bin/env python3
"""Validate the portable AI drama router package without host dependencies."""

from __future__ import annotations

import sys
from pathlib import Path


ROUTER_REFERENCES = (
    "canon-boundary.md",
    "routing-matrix.md",
    "skill-resolution-policy.md",
    "drama-route-plan-contract.md",
    "route-examples.md",
)

REQUIRED_SKILL_NAMES = (
    "ai-drama-format-strategist",
    "ai-drama-context-pack-builder",
    "ai-drama-story-architecture",
    "ai-drama-character-engine",
    "ai-drama-showrunner",
    "screenplay-scene-writer",
    "ai-drama-director",
    "ai-drama-video-reference-director",
    "ai-drama-visual-language",
    "ai-drama-edit-and-sound",
    "ai-drama-continuity-supervisor",
    "ai-drama-critic-panel",
    "ai-drama-producer",
    "ai-drama-production-orchestrator",
    "creative-style-lens-builder",
)

def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    script_path = Path(__file__).resolve()
    router_dir = script_path.parents[1]
    references_dir = router_dir / "references"

    for reference in ROUTER_REFERENCES:
        if not (references_dir / reference).is_file():
            fail(f"missing router reference: {reference}")

    skill_text = (router_dir / "SKILL.md").read_text(encoding="utf-8")
    matrix_text = (references_dir / "routing-matrix.md").read_text(encoding="utf-8")
    combined_contract = skill_text + "\n" + matrix_text

    for skill_name in REQUIRED_SKILL_NAMES:
        if f"`{skill_name}`" not in combined_contract:
            fail(f"routing contract does not reference required skill: {skill_name}")

    if "一个 primary" not in skill_text or "最多一个" not in skill_text:
        fail("router must preserve the one-primary/one-constraint invariant")
    if "approved_current_request" not in (
        references_dir / "skill-resolution-policy.md"
    ).read_text(encoding="utf-8"):
        fail("activation policy must preserve explicit current-request authorization")

    print("PASS: portable AI drama router package is structurally valid")


if __name__ == "__main__":
    main()
