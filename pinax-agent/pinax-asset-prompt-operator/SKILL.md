---
name: pinax-asset-prompt-operator
description: Use when an agent needs to manage Pinax assets, note attachments, prompt assets, content collections, or local prompt/asset graph projections through bounded Pinax commands.
---

# Pinax Asset Prompt Operator

Operate Pinax media/binary assets, note attachments, prompt assets, content collections, and graph projections. These workflows keep payloads in the vault or user-requested output files while command projections stay bounded.

## Use When

- The request mentions `pinax asset`, images, PDFs, binary assets, `note attach`, note attachments, prompt assets, `pinax prompt`, content bundles, `pinax collection`, or `pinax graph`.
- The user wants to import/export prompt bundles, resolve a prompt URI, inspect prompt graph context, or attach a local file to a note.
- The command family is `pinax asset`, `pinax note attach`, `pinax note attachments`, `pinax prompt`, `pinax collection`, or `pinax graph`.

## Command Patterns

```bash
pinax asset add ./diagram.png --vault ./my-notes --json
pinax asset list --vault ./my-notes --agent
pinax asset show diagram.png --vault ./my-notes --json
pinax asset link diagram.png --note "Auth Plan" --vault ./my-notes --json
pinax asset backlinks diagram.png --vault ./my-notes --json
pinax asset missing --vault ./my-notes --json
pinax asset repair --plan --vault ./my-notes --json
pinax asset verify --vault ./my-notes --json
pinax note attach "Auth Plan" ./diagram.png --placement note-folder --embed --vault ./my-notes --json
pinax note attachments "Auth Plan" --include-paths --vault ./my-notes --json
pinax prompt import --from ./novel-character.yaml --vault ./my-notes --json
pinax prompt search "character portrait" --domain visual_generation --vault ./my-notes --json
pinax prompt resolve pinax://prompt/novel_character_portrait_v1 --vault ./my-notes --agent
pinax prompt lifecycle novel_character_portrait_v1 --to tested --reason "fixture render passed" --vault ./my-notes --json
pinax collection import --from ./bundle.json --dry-run --vault ./my-notes --json
pinax collection import --from ./bundle.json --yes --vault ./my-notes --json
pinax collection export --to ./eikona-bundle.json --format eikona.prompt_bundle.v1 --vault ./my-notes --json
pinax graph rebuild --vault ./my-notes --json
pinax graph query --kind technique --match storyboard --vault ./my-notes --json
```

## Workflow

1. Inspect before writes with `pinax asset list`, `pinax asset show`, `pinax note attachments`, `pinax prompt search`, `pinax collection doctor`, or `pinax graph query`.
2. For note-local files, prefer `pinax note attach` so the note reference and asset metadata stay consistent.
3. For vault-wide asset metadata, use `pinax asset add/link/move/remove/repair/verify`; do not edit manifests by hand.
4. For prompt assets, import schemas through `pinax prompt import` and resolve through `pinax prompt resolve pinax://prompt/<id> --agent` instead of reading SQLite or metadata files.
5. For content bundles, run `collection import --dry-run` and `collection doctor` before `collection import --yes`.
6. Rebuild graph projections only when needed; they are rebuildable local projections, not proof of provenance.
7. Require explicit approval for moving, removing, lifecycle promotion/retirement, or bundle import with `--yes`.

## Safety Boundaries

- Do not print binary payloads, full prompt bodies, raw provider payloads, hidden prompts, private tool arguments, secrets, or full chain-of-thought in command projections or notes.
- Do not hand-edit `.pinax/assets/**`, prompt projection rows, collection receipts, or graph projection files.
- `collection export` may write prompt bodies only to the user-requested output file; summaries should remain bounded.
- Pinax stores prompt assets and evidence; it does not execute Eikona, crawl sources, or render images.

## Validation

- After asset changes: `pinax asset verify --vault <vault> --json`.
- After attachment changes: `pinax note attachments "<note>" --vault <vault> --json`.
- After prompt imports: `pinax prompt resolve pinax://prompt/<id> --vault <vault> --agent`.
- After collection import or graph rebuild: `pinax collection doctor --from <bundle> --json` or `pinax graph query --kind <kind> --match <term> --json`.
