---
name: golang-goreleaser-distribution
description: Use when configuring, reviewing, or documenting GoReleaser distribution for Go projects, including Homebrew, Scoop, Chocolatey, nFPM DEB/RPM/APK packages, APT repository decisions, GitHub release workflows, cross-repository publish tokens, signing, SBOMs, and attestations.
---

# Golang GoReleaser Distribution

## When to Use

Use this for Go projects that mention GoReleaser package-manager distribution, Homebrew, Scoop, Chocolatey, `.deb`, `.rpm`, `.apk`, APT/yum/alpine repositories, release artifacts, release CI, publisher tokens, signing, SBOM, attestations, or post-release install smoke.

**REQUIRED SIBLING:** use `golang-github-release-guardrails` first for baseline CI/lint/tag rules. This skill owns distribution-channel details, cross-repository publisher credentials, package signing, SBOMs, attestations, and install verification.

## Inputs

Before designing or changing distribution, read:

- `go.mod`
- Existing `.goreleaser.yaml` or `.goreleaser.yml`
- `.github/workflows/*.yml` and `.github/workflows/*.yaml`
- Release docs, packaging docs, and Taskfile release tasks
- Existing package names and binary names
- GitHub release repository owner/name
- Homebrew tap and Scoop bucket repository names
- Available GitHub environments, secrets, and variables

Do not invent a second buildinfo, version, token, or release branch convention beside one that already exists in the project.

## Release Ref Policy

- `develop`, PRs, `workflow_dispatch`, and optional `release/*` branches are CI/snapshot/release-candidate only.
- Official publish only from semver tags on stable code:
  - Standalone repos use `vX.Y.Z` or `vX.Y.Z-prerelease.N`.
  - Root monorepo workflows may use `<project>/vX.Y.Z` only when the existing workflow already uses project-prefixed tags.
- `workflow_dispatch` must run:

  ```bash
  goreleaser release --snapshot --clean --skip=publish
  ```

- Release workflows keep top-level `permissions: contents: read`.
- Only the publish job escalates to `contents: write`.
- Add `id-token: write` only for cosign/OIDC.
- Add `attestations: write` only when using `actions/attest`.
- Never publish real releases directly from broad branch patterns such as `main`, `develop`, `release/*`, or “non-test branches”.

## Distribution Matrix

| Channel | Decision |
| --- | --- |
| Archives | Always generate Linux/macOS tarballs and Windows zip archives for `amd64` and `arm64` unless the project has a documented unsupported platform. |
| Checksums | Always generate SHA-256 checksums with a predictable filename: `checksums.txt` for attestation-friendly configs, or `<project>_<version>_checksums.txt` when matching existing project style. |
| Source archive | Enable for public/user-facing CLI distribution. |
| SBOM | Enable `sboms` for archive artifacts for user-facing distribution. |
| Linux packages | Use `nfpms` for `.deb`, `.rpm`, and `.apk`; install binaries to `/usr/bin`; include license/readme docs under `/usr/share/doc/<project>` or `/usr/share/licenses/<project>`. |
| APT repository | Do not claim nFPM alone creates an APT repository. If a real APT/yum/alpine repository is required, use GoReleaser Pro Cloudsmith or a separately approved repository publisher with its own token. Otherwise publish `.deb` as a GitHub Release asset and document direct package install. |
| Homebrew | Default to `homebrew_casks`, copying the `cli/skillctl/.goreleaser.yaml` pattern. Use legacy `brews`/Formula only when an existing project already relies on formula semantics. Do not add both cask and formula for the same binary without an explicit project decision. |
| Scoop | Use `scoops`, `yeisme/scoop-bucket`, and `directory: bucket` to match existing Yeisme configs. |
| Chocolatey | Use `chocolateys` to generate `nupkg`; keep `skip_publish: true` in first-pass configs unless `CHOCOLATEY_API_KEY`, package metadata, and moderation readiness are explicitly present. |

## Credential Policy

- Same-repository GitHub Release only: use `${{ secrets.GITHUB_TOKEN }}` and job `permissions.contents=write` only in the release job.
- Cross-repository Homebrew/Scoop publishing: prefer a per-project GitHub App named `yeisme-<project>-release-publisher`.
  - Store `RELEASE_APP_CLIENT_ID` as a `release` environment variable.
  - Store `RELEASE_APP_PRIVATE_KEY` as a `release` environment secret.
  - Mint a short-lived token in the release job with `actions/create-github-app-token@v3`.
  - Pass it to GoReleaser as `PUBLISHER_TOKEN`.
  - Reference it from `homebrew_casks.repository.token` and `scoops.repository.token`.
- GitHub App installation repository selection: include only target publish repositories: `homebrew-tap`, `scoop-bucket`, and any project-specific package-manifest repository. Add the source project repository only if the app token is also used as GoReleaser `GITHUB_TOKEN` for GitHub Release creation.
- GitHub App permissions: `contents: write` only. Add `pull_requests: write` only if GoReleaser PR mode is enabled. Do not grant `administration`, `actions`, `secrets`, `workflows`, `issues`, or `packages` unless a named GoReleaser feature in the same config requires it.
- Fine-grained PAT fallback: use only if a GitHub App cannot be created. Name the secret `PUBLISHER_TOKEN`, restrict selected repositories to the exact source/tap/bucket set, grant `contents: write`, set an expiration, and store it only in the protected `release` environment:

  ```bash
  gh secret set PUBLISHER_TOKEN --env release
  ```

- `gh secret set` and `gh variable set` store existing values; they do not generate keys or tokens.

## Required Workflow Shape

Use this shape for new workflows. If the project already has a GoReleaser workflow, adapt it without mixing action major versions.

```yaml
permissions:
  contents: read

jobs:
  snapshot:
    if: github.event_name == 'workflow_dispatch'
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          persist-credentials: false
      - uses: actions/setup-go@v5
        with:
          go-version-file: go.mod
      - uses: goreleaser/goreleaser-action@v7
        with:
          distribution: goreleaser
          version: "~> v2"
          args: release --snapshot --clean --skip=publish

  release:
    if: startsWith(github.ref, 'refs/tags/v')
    environment: release
    permissions:
      contents: write
      id-token: write # only when cosign/OIDC is configured
      attestations: write # only when actions/attest is configured
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          persist-credentials: false
      - uses: actions/setup-go@v5
        with:
          go-version-file: go.mod
      - id: publisher-token
        # Include this step only in cross-repository tap/bucket workflows.
        uses: actions/create-github-app-token@v3
        with:
          client-id: ${{ vars.RELEASE_APP_CLIENT_ID }}
          private-key: ${{ secrets.RELEASE_APP_PRIVATE_KEY }}
          owner: ${{ github.repository_owner }}
          repositories: |
            homebrew-tap
            scoop-bucket
      - uses: goreleaser/goreleaser-action@v7
        with:
          distribution: goreleaser
          version: "~> v2"
          args: release --clean
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          PUBLISHER_TOKEN: ${{ steps.publisher-token.outputs.token }}
```

If an existing project is pinned to `goreleaser/goreleaser-action@v6`, do not silently mix versions in one workflow. Either keep v6 in that project-specific change or upgrade all GoReleaser Action uses in that workflow as a separate explicit release-maintenance step. Never use `latest`.

For same-repository-only release workflows, omit the `publisher-token` step, omit the `PUBLISHER_TOKEN` environment variable, and remove `repository.token: "{{ .Env.PUBLISHER_TOKEN }}"` from Homebrew/Scoop config.

## Required GoReleaser Shape

Use this shape for new distribution configs, then replace placeholders with project values. Copy the owning project's existing `ldflags`/buildinfo convention when one exists (`pkg/buildinfo`, `internal/build`, or `main` vars); do not invent a second convention.

```yaml
version: 2
project_name: <project>

builds:
  - id: <project>
    binary: <project>
    env:
      - CGO_ENABLED=0
    flags:
      - -trimpath
    ldflags:
      - -s -w
    goos: [linux, darwin, windows]
    goarch: [amd64, arm64]

archives:
  - id: bundles
    ids: [<project>]
    formats: [tar.gz]
    format_overrides:
      - goos: windows
        formats: [zip]

checksum:
  name_template: checksums.txt
  algorithm: sha256

source:
  enabled: true

sboms:
  - artifacts: archive

nfpms:
  - id: linux-packages
    ids: [<project>]
    package_name: <project>
    formats: [deb, rpm, apk]
    bindir: /usr/bin
    license: MIT

homebrew_casks:
  - name: <project>
    repository:
      owner: yeisme
      name: homebrew-tap
      token: "{{ .Env.PUBLISHER_TOKEN }}"
    directory: Casks
    binaries: [<project>]
    skip_upload: "{{ .IsSnapshot }}"

scoops:
  - name: <project>
    repository:
      owner: yeisme
      name: scoop-bucket
      token: "{{ .Env.PUBLISHER_TOKEN }}"
    directory: bucket
    skip_upload: "{{ .IsSnapshot }}"
```

## Signing, SBOM, and Attestations

- Require SBOMs for user-facing distribution.
- Prefer cosign keyless archive/checksum signing over long-lived signing keys.
- Use nFPM GPG package signatures only when the project already has `GPG_KEY_PATH`/GPG secret handling or the release task explicitly adds it.
- Use `actions/attest@v4` after GoReleaser when `checksums.txt` is predictable.
- Verify attestations with:

  ```bash
  gh attestation verify --owner <owner> <filename>
  ```

## Post-release Verification

Every release-distribution change needs at least one archive checksum verification and one install smoke. Follow the `cli/skillctl/docs/ci-cd.md` pattern:

```bash
gh release download <tag> --repo <owner>/<repo> --pattern '*checksums.txt' --pattern '*linux*amd64*'
sha256sum --check checksums.txt --ignore-missing
go install <module>@<tag>
<binary> --version
<binary> --help
```

For Homebrew/Scoop changes, add smoke checks when the tap or bucket is reachable:

```bash
brew install yeisme/tap/<project>
brew test yeisme/tap/<project>
scoop bucket add yeisme https://github.com/yeisme/scoop-bucket
scoop install <project>
<project> --version
```

If a project is not public/go-installable, replace `go install <module>@<tag>` with an install path the release docs already support.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Using one broad classic PAT so release “just works” | Use `GITHUB_TOKEN` for same-repo releases and a per-project GitHub App token for cross-repo taps/buckets; fine-grained PAT is fallback only. |
| Publishing real releases from `main`, `develop`, `release/*`, or “non-test branches” | Branches/manual dispatch are snapshots only; official publish requires semver tags on stable code. |
| Using `latest` for GoReleaser Action or tool versions | Pin a major action version and GoReleaser `"~> v2"`; keep existing action major consistent within one workflow. |
| Hand-editing `.agents/skills/` or `.claude/skills/` runtime copies | Edit `.skills/yeisme/` source only, then run skill sync. |
| Claiming `.deb` equals APT repository support | nFPM creates `.deb` assets. A real APT repository needs Cloudsmith or another approved repository publisher. |
| Publishing Chocolatey test packages publicly | Generate `nupkg` first; keep `skip_publish: true` until API key, metadata, and moderation readiness exist. |
| Adding package-manager install scripts that mutate global skills/runtime state | Keep release packaging focused on project binaries and package manifests; skills/runtime sync belongs to skill tooling. |
