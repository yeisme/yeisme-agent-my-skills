---
name: pinax-template-authoring-operator
description: Use when an agent needs to manage Pinax Markdown templates, template-backed note creation, template previews/renders/runs, index pages, inbox/draft review indexes, or journal/template authoring workflows.
---

# Pinax Template Authoring Operator

Operate Pinax templates and template-authored notes. Templates are CLI-managed assets; preview and recommendation commands are read-only, while create/render/index page writes must go through Pinax commands.

## Use When

- The request mentions `pinax template`, a note template, sticky/idea/learning templates, `note add --template`, index pages, inbox/draft review indexes, or journal template workflows.
- The user wants to create repeatable note structures, preview a template, render content, or create managed index pages.
- The command family is `pinax template`, `pinax note add --template`, `pinax index page`, `pinax inbox index`, `pinax draft index`, or template-assisted `pinax journal` use.

## Command Patterns

```bash
pinax template init --vault ./my-notes --json
pinax template list --vault ./my-notes --json
pinax template recommend --intent "论文" --vault ./my-notes --json
pinax template show idea.research_seed --vault ./my-notes --json
pinax template inspect idea.research_seed --vault ./my-notes --json
pinax template validate weekly --vault ./my-notes --json
pinax template preview weekly --title "Client Meeting" --var client=Acme --vault ./my-notes --agent
pinax template render weekly --title "Client Meeting" --save-run weekly-demo --vault ./my-notes --json
pinax note add "某篇小说是怎么写成的" --template idea.research_seed --dir index --vault ./my-notes --json
pinax note add "临时线索" --template sticky.capture --dir index --vault ./my-notes --json
pinax journal daily append --body "Template result summary" --vault ./my-notes --json
pinax index page preview ideas --template index.ideas --vault ./my-notes --json
pinax index page create ideas --template index.ideas --vault ./my-notes --json
pinax inbox index preview --vault ./my-notes --json
pinax draft index refresh --vault ./my-notes --json
```

## Workflow

1. Use `pinax template recommend --intent "..." --json` before inventing a new template name.
2. Inspect and validate templates before rendering: `pinax template inspect <name> --json` and `pinax template validate <name> --json`.
3. Use `pinax template preview` for read-only review. Use `template render --save-run` only when a render receipt is useful.
4. For agent-authored notes created from templates, still follow the intake rule: pass `--dir index` unless the user named a final destination or an approved template output path is explicitly intended.
5. Use `pinax index page preview` before `create` or `refresh`; use `pinax inbox index` and `pinax draft index` for their specialized managed pages.
6. Do not hand-write `.pinax/templates/**`, render receipts, managed index blocks, or template metadata.

## Safety Boundaries

- Template functions are allowlisted; do not ask templates to execute scripts, read environment variables, or call the network.
- `schema_version: pinax.template_design.v1` templates are design drafts; do not use them for executable note creation until published as executable templates.
- Template previews are read-only. If an index is stale, run an explicit index command instead of silently writing.
- Generated notes should not contain secrets, raw prompts, provider payloads, hidden prompts, or full chain-of-thought.

## Validation

- Before writing: `pinax template preview <name> --json` or `pinax index page preview <name> --json` succeeds.
- After template note creation: `pinax note show "<title>" --json` or `pinax search "<title>" --json` finds the note.
- After managed index writes: run the matching preview command again.
