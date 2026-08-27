---
name: credentialctl-usage
description: Use when operating credentialctl for user-level shared credentials or repository project secrets, including setup, rotation, status, machine output, completion, metadata, diagnosis, and internal release verification.
---

# Credentialctl usage

Use this skill only for the local single-user `credentialctl` trust boundaries. It never authorizes exposing, copying, logging, or returning a secret.

## Choose the secret plane

- Use `setup`, `set`, `rotate`, `status`, `doctor`, `enable`, `disable`, and `remove` for user-level credentials shared by approved local Yeisme consumers.
- Use `project init`, `project secret`, `project unlock`, `project rekey`, and `project exec` for encrypted repository project secrets.
- Never put endpoint, model, budget, provider profile, OAuth refresh token, production/admin/payment secret, or server credential into the shared registry.

## Cross-project adoption

- Treat `cli/credentialctl/docs/integration.md` as the canonical integration guide.
- Activate this skill through the root target profile and `scripts/skills.sh sync-target`; never copy a runtime skill directory by hand.
- The `local-ai` preset currently grants only `eikona/image`, `pinax/embedding`, `aigora/text`, `scaena/video`, and `anatomia/service`.
- Skill availability does not grant secret access. A new consumer or capability requires an owning credentialctl OpenSpec change and policy tests.
- Non-Go projects should call the CLI. Go owners may import only `pkg/credentials`, `pkg/localstore`, or `pkg/projectsecrets`; never import or copy `internal/store`.
- Browser, UI, facade, and shared broker code may consume redacted readiness only and must never resolve secret bytes.

## Safe input

- Prefer hidden TTY input for people.
- For automation, pipe the secret through stdin. Never add a plaintext secret flag or place it in argv.
- `setup` is create-if-absent and never overwrites. Use `rotate` for an existing ref.
- Destructive non-interactive operations require `--yes`.
- Project unlock configuration is explicit for each invocation and is never stored in `.yeisme/credentialctl.yaml`.

## Read-only diagnosis

1. Run `credentialctl status [ref] --json`; this is local-only.
2. Run `credentialctl doctor [ref] --json`; add `--probe` only when provider network validation is explicitly required.
3. Follow only the redacted `actions` in the `1.0` envelope.
4. Treat `partial` as completed diagnosis requiring attention, not as permission to retrieve a secret.

## Machine output

- `--json`: one `spec_version=1.0` envelope; command data lives under `data`.
- `--agent`: single-line-safe `key=value`; never parse it as JSON.
- `--events`: ordered NDJSON using `type`, `seq`, `spec_version`, and `command`.
- `--explain`: redacted decision report, not chain-of-thought.
- The modes are mutually exclusive. `completion`, `--version`, and `project exec` use documented raw transports.

## Project metadata

`.yeisme/credentialctl.yaml` may contain only schema version, project identity, repository identity, and contained asset path. It is not a secret store. Use `project metadata show` to inspect it and `project metadata write` for idempotent repair.

## Release boundary

`v0.2.0` is published as a GitHub Release under the owner's explicit authorization recorded on 2026-08-27. The repo is private and has no LICENSE file yet (`license_status=unresolved`): do not redistribute artifacts outside the owning organization until a license is added.

Before claiming a candidate is ready, run the repository Task/OpenSpec/redaction/release checks and require native Windows/macOS evidence. Never copy evidence containing secrets or private absolute paths into chat or documentation.
