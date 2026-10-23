# DriveBridge knowledge workspace operator reference

Use this reference when the request concerns the DriveBridge knowledge base, notebook pages, resource descriptors, Skills, templates, or Pinax reading.

## Read path

1. Read the installed capabilities and the owner input schema.
2. Fix the scope to the current actor, tenant, space, source, object and revision.
3. Read notebook metadata or a resource descriptor before requesting body bytes.
4. Treat pagination, `scanned`, `unavailable`, `stale`, and `next_cursor` as facts about the observed slice only.
5. Open a fixed version explicitly; a newer head is a new read, not a silent replacement.

For CLI users:

```bash
drivebridge capabilities --json
```

The CLI command above is discovery only. Notebook, resource and Pinax actions are available only when the installed client advertises their contracts.

## Write and recovery path

- Ordinary Markdown: keep the draft in memory or the local draft store, show a diff, and save with `base_version_id`/expected revision after human confirmation.
- Offline or service unavailable: retain the draft as `waiting for sync`; do not claim that the Server saved it.
- Version conflict: read the service version and the recorded base, present a three-way merge, and save the selected result with the owner contract.
- Lost response or unknown mutation: query the original operation/receipt using the same idempotency key. Do not submit a replacement request.
- Permission loss or context change: clear body, snippets, media and hidden names; retain only a safe recovery message.

## Page tree and daily pages

`parent_file_id`, page icon, daily date, path and revision are Server-owned metadata. A selected parent only constrains a create request; it does not grant write access. Cycle prevention, duplicate paths and idempotent create recovery belong to the application service.

## Skill and resource boundary

`skill`, `template` and `reference_pack` are resource descriptor kinds. A descriptor or snapshot can be inspected and checked, but:

- it does not execute embedded scripts;
- it does not install or publish a Skill;
- it does not authorize a provider call or paid analysis;
- it does not make a Chinese review translation an Agent-compilable template;
- it does not move canonical content out of `.skills/yeisme/` or Template Registry.

Keep descriptor/member versions fixed. A later resource head must not rewrite an earlier snapshot's contents.

## Pinax boundary

DriveBridge Web does not read `.pinax/**`, a local vault path, or a bearer token. Pinax note identity, relationships and reader permissions come from the Pinax owner contract. Without a desktop reader binding or managed-vault guard, report `unsupported`/`unavailable` and keep the ordinary Markdown path separate.

## Verification

Run focused checks from the DriveBridge root and keep the existing evidence boundary:

```bash
python3 scripts/check.py -- pnpm --dir web exec vitest run src/features/notebook/KnowledgePage.test.tsx src/features/notebook/NotebookPageTree.test.tsx src/features/resources/ResourcesPage.test.tsx src/features/resources/ResourceIntegrity.test.tsx
openspec validate drivebridge-personal-workspace-rebuild-v1 --strict --no-interactive
git diff --check
```

These checks do not prove real Pinax, cloud storage, Skill installation/execution, Electron hardware, or release readiness.

## Web feature ownership

The formal Web entry remains `WorkspaceApp` plus the existing lazy route table. Notebook and Resources use separate page feature layers:

```text
features/notebook or features/resources/
├── contract.ts
├── projection.ts
├── state.ts
├── clients/
├── recovery/
└── components/
```

`contract.ts` keeps fixed identity, revision and lifecycle states; `projection.ts` is a pure safe DTO projection; `state.ts` contains only local UI state; `clients/` wraps the existing owner HTTP/generated contracts; `recovery/` owns the original operation, receipt, idempotency and local recovery rules. Pages do not own canonical content or credentials. Cross-feature fixed-member reading goes through `consumer-flows/public.ts`; do not import another feature's private component or client.

Compatibility re-exports are allowed while historical paths are migrated. A missing reader binding, managed-vault guard or owner capability remains `unsupported`/`unavailable`. Do not add a second page database, route system, Server API, or Pinax access path.
