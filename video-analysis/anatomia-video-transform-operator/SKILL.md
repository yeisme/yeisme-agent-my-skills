---
name: anatomia-video-transform-operator
description: Use when deriving grayscale numeric sequences, detecting/materializing shots, or extracting per-purpose placeholder keyframes from an authorized local video with the Anatomia CLI.
---

# Anatomia Video Transform Operator

Run one bounded local transform on one authorized local video: `anatomia video grayscale derive --source /absolute/path/shot.mp4 --start 500000 --end 4500000 --to ./gray-out --json`, `anatomia video shots detect --source /absolute/path/ep1.mp4 --source-ref source:ep1 --to ./shot-list.json --agent`, or `anatomia video placeholders extract --source /absolute/path/ep1.mp4 --source-ref source:ep1 --shot-ref source:ep1:shot:0 --start 500000 --end 1500000 --purpose thumbnail,character --agent`.

Install this skill with `npx skills add yeisme/yeisme-agent-my-skills --skill anatomia-video-transform-operator --agent codex --copy --full-depth -g -y`. Skills do not install the `anatomia` binary or ffmpeg.

These are local deterministic transforms, not model analysis: no provider is called and nothing enters an evidence bundle automatically. Grayscale utility output always carries `evidence_binding=none`. Shot lists are segmentation evidence, never a production storyboard; canonical storyboard review/freeze belongs to Scaena. Commands: `references/commands.md`. Troubleshooting and boundaries: `references/handoff.md`.
