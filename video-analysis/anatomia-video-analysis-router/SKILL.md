---
name: anatomia-video-analysis-router
description: Use when logging in with an Anatomia service access key and analyzing an authorized local video through the Anatomia CLI.
---

# Anatomia Video Analysis Router

Log in, then analyze one authorized file: `anatomia login --endpoint https://anatomia.example.com --key-file /absolute/private/anatomia-access.key` then `anatomia analyze file --file /absolute/path/demo.mp4 --to ./anatomia-output/demo --json`.

Install this skill with `npx skills add yeisme/yeisme-agent-my-skills --skill anatomia-video-analysis-router --agent codex --copy --full-depth -g -y`. Skills do not install the `anatomia` binary or any key.

Hand a registered-ref question to `$anatomia-video-evidence-navigator`, review to `$anatomia-storyboard-reviewer`, and export to `$anatomia-asset-handoff-builder`. Model output is a candidate observation, not an accepted fact. Commands: `references/commands.md`. Handoff: `references/handoff.md`.
