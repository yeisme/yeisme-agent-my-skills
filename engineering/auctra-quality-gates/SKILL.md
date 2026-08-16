---
name: auctra-quality-gates
description: Use when changing, testing, reviewing, or documenting code quality, CI/CD, lint debt, release gates, or integration evidence for cli/auctra.
---

# Auctra Quality Gates

Use this skill in `cli/auctra` when a change affects implementation quality,
lint policy, local verification, GitHub Actions, release automation, or
integration-test evidence. Read `cli/auctra/AGENTS.md` and the active OpenSpec
change before editing.

## Working rules

- Preserve Auctra's CLI, review, provider-boundary, and evidence contracts.
- Start with `git status --short` and record pre-existing changes; do not reset,
  clean, publish, or release from the agent session.
- Prefer low-risk, behavior-preserving fixes. Do not use a global lint disable
  or a broad path exclusion to hide historical debt.
- Historical lint debt may be excluded only by exact file-level rules, with a
  short reason and a follow-up OpenSpec task. New or low-risk rules should be
  blocking.
- Report a slow or interrupted race run as interrupted; never present it as a
  passing verification.
- Integration evidence belongs under
  `temp/integration-test-runs/<run-id>/` and must redact secrets, tokens,
  provider payloads, private tool arguments, and full model reasoning.

## Recommended loop

From `cli/auctra` run the narrowest relevant checks first:

```bash
task fmt-check
task lint
task test
task test-race
task vet
task security
task ci
task test:integration
task release:verify
```

Use `task ci` as the reproducible local quality gate. Use `task check` when a
broader developer gate is required, and use `task release:verify` before a tag
or release workflow review. Validate the owning OpenSpec change with:

```bash
openspec validate auctra-code-quality-cicd-v1 --strict --no-interactive
```

## CI/CD review checklist

- Go, golangci-lint, govulncheck, GoReleaser, and Syft versions are explicit.
- CI jobs have bounded timeouts and cancel stale pull-request runs.
- Release publishing is tag-only and manual snapshot builds do not publish.
- Release smoke tests remain non-interactive: `--version`, `--help`, and
  `runtime doctor --json`.
- The final report names passed, failed, skipped, and interrupted gates plus
  the evidence directory for integration tests.
