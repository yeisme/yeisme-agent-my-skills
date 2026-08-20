---
name: anatomia-storyboard-reviewer
description: Use when validating, reviewing, freezing, or forking an Anatomia storyboard revision.
---

# Anatomia Storyboard Reviewer

Validate then freeze a reviewed revision: `anatomia revision validate revision:demo --json` then `anatomia revision freeze revision:demo --expected-version 3 --reviewer reviewer:owner --evidence review-receipt:demo --json`.

Never edit accepted structured state by hand. Frozen revisions are immutable; later edits use fork. Commands: `references/commands.md`. Handoff: `references/handoff.md`.
