---
name: private-release
description: Use when creating, configuring, reviewing, or executing a formal release for any private Yeisme product repository, including release workflow design, private distribution channels, token-authenticated installs, tag failure recovery, or adopting the Yeisme private release reference in a new project.
---

# Private Release

## Purpose

Ship formal releases from **private** repositories without ever requiring the repository (or its channels) to become public. This skill is the operator guide for the Yeisme private release reference (`docs/operations/private-release-reference.md` in the root repo; Eikona `docs/delivery/release-distribution.md` is the landed reference implementation).

## Principles

1. Product repo, homebrew tap, and scoop bucket stay private. Only deliberately public derivative repos (for example `yeisme-agent-my-skills` and the binary mirror `yeisme/yeisme-dist`) may be public, and release-time checkouts must never depend on the private monorepo.
2. Installs authenticate on the **private** channel: `<PRODUCT>_RELEASE_TOKEN` first, then `gh auth token`. The bearer token is attached only to `github.com` / `api.github.com` hosts — never to test endpoints or third-party domains. Anonymous public installs use `yeisme/yeisme-dist` and must not require a token.
3. Private asset downloads must use the GitHub API asset endpoint with `Accept: application/octet-stream`; the `releases/download/...` browser URL rejects bearer tokens on private repos (anonymous-style 404).
4. Provenance does not depend on GitHub attestations (unavailable on user-owned private repos): gate attestations on `github.event.repository.visibility == 'public'`; private integrity = checksums + SBOM + per-asset sha256 in the install manifest.
5. A failed tag is burnt: delete the draft release and tag, revert the tap/bucket manifests for that version, fix, and cut the next patch tag. Never reuse a tag whose run touched the channels.

## Procedure

1. **Pre-flight (local)**: `go mod tidy -diff`, `task fmt-check`, `task lint`, full tests, `go vet`, govulncheck, `goreleaser check`, `goreleaser release --snapshot --clean --skip=publish`. These mirror CI; any drift blocks the release.
2. **Push and wait**: develop CI must be green on the exact commit to tag.
3. **Tag**: `git tag -a vX.Y.Z -m "<product> vX.Y.Z" && git push origin vX.Y.Z`. The release workflow builds, verifies, and publishes; it must not require cross-repo private checkouts.
4. **Verify (private)**: download assets + `sha256sum --check checksums.txt --ignore-missing`, `--version`, installer plan/apply/doctor with a token, fixture smoke.
5. **Verify (public mirror)**: product release workflows should dispatch `product-release` to `yeisme/yeisme-dist` when `DIST_SYNC_TOKEN` is set on the product repo. Then anonymous-install from dist:

   ```bash
   gh secret set DIST_SYNC_TOKEN --repo yeisme/<product>   # reuse the same PAT already on yeisme-dist
   env -u GH_TOKEN -u GITHUB_TOKEN curl -fsSL https://raw.githubusercontent.com/yeisme/yeisme-dist/main/install.sh | bash -s <name>
   ```

   First-time products: append `name|yeisme/<repo>|<optional-tag-prefix>` to `products.txt` (zero-asset rows are skipped). Copy the `Notify yeisme-dist` step from an existing release workflow. Do not add a product with no publish pipeline.
6. **On failure**: capture the failing step, clean the burnt tag (draft + tag + channel manifests), fix on develop, repeat with the next patch version. Do not delete a successful dist mirror of an older version.

## Reference implementations

- Eikona: `.github/workflows/eikona-release.yml`, `scripts/eikona-skills-bundle.sh`, `internal/installer/release_auth.go` (credential resolution, github-scoped bearer transport, API asset endpoint switch, anonymous 401/404 guidance).
- Channel matrix, onboarding checklist, public mirror (`yeisme/yeisme-dist`), and measured pitfalls: root `docs/operations/private-release-reference.md`.

## Verification evidence to keep

- Green CI run id on the tagged commit.
- Release URL with asset count; checksum verification output.
- Installer plan/apply/doctor output in a temporary HOME using the token (not committed secrets — redacted logs only).
