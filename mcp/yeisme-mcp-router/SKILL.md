---
name: yeisme-mcp-router
description: "Use when an agent is about to operate any Yeisme MCP surface — eikona mcp, gitea-mcp through the Gateway, cloudflare-api backends, or scaena mcp — and must pick the right operating skill, verify tool/action names before first use, or recover from slow multi-round MCP fumbling. Route-only: connection setup, tokens, approvals, and server administration stay in the dedicated skills."
---

# Yeisme MCP router

Yeisme MCP surfaces hide large catalogs behind compact tool faces
(`eikona.execute`: 78 actions; `gitea_mcp_exec`: ~370 actions). The dominant
slowness is not the network — it is agents fumbling with guessed names,
missing arguments, and repeated discovery calls. Route to the narrowest
operating skill and follow its first-call verification; do not improvise
against the MCP surface directly.

## Routing table

| Intent | Go to | Why |
| --- | --- | --- |
| Generate/edit an image via Eikona; artifact delivery and download recovery | `eikona-mcp-image` | Direct `eikona.execute generate/edit` fast path; no catalog scans first |
| Any other Eikona MCP action (review, feedback, assets, library, workflow, delivery, comparison, dataset, evidence writeback, operator diagnostics) | `eikona-mcp-actions` | Intent→action navigation map with lanes and shortest sequences |
| Operate Gitea (repos, issues, PRs, branches, CI runs) through `gitea_mcp_*` or a direct gitea-mcp server | `gitea-mcp-quickstart` | Two-call golden path: `search` → copy `exec_example` → `exec` |
| Connect to a Gateway endpoint, tokens/OAuth, discovery, approvals, peer-origin failures | `yeisme-mcp-gateway-consumer` | Connection and policy layer, not action operation |
| Administer a deployed Gateway (catalog, revisions, approvals, packs) | `yeisme-mcp-gateway-operator` | Operator action surface |
| Build or change a self-built MCP server under this repository | `yeisme-mcp-builder` | Author-side minimal-tool-face and token-budget rules |
| Add/update a backend in `mcp/registry.json` | `yeisme-mcp-registry-onboarding` | Registry onboarding governance |
| Configure Codex against the Gateway | `codex-agent-runtime` | Gateway-rendered client config, tool-name mapping |
| Configure Codex against a direct Eikona LAN `/mcp` URL | `eikona-mcp-image` then `codex-agent-runtime` | Owner HTTP MCP, not Gateway; remote edit forbids client local paths |
| Scaena official MiniMax H3 / Wan3 video generation, upload or task recovery | `scaena-production-operator`; `tools/list`, `scaena.search`, `scaena://video-tasks/guide` | Use `createVideoProviderTask` with explicit official binding; no Aigora base URL or shot preflight. Include unavailable results for schema/recovery only. |
| Other Scaena MCP operations | `tools/list` and readable capability resources; optional installed CLI discovery | Confirm exact live actions and scopes before execute; do not invent tool names. |
| auctra mcp text-creation operations | `auctra.search` + `auctra.execute` compact pair | Diagnostic entry is `auctra mcp capabilities --json`; unknown and not-yet-backed actions share one error, so read the `auctra://authoring/capabilities` resource instead of guessing; mutations require idempotency_key and never write canonical text |
| Personal OneDrive/S3 creative file upload/download, `drivebridge://file/<id>` reference handoff to Scaena, or成品回存 (`save_output`) | `drivebridge-operator`; preflight `drivebridge doctor`, discover `drivebridge capabilities --json` or `drivebridge://capabilities` | Local stdio per machine, default off without `--enabled`; stable refs only — bytes move over owner transport, transient URLs never enter MCP output. Not the lark-drive (飞书云空间) or pinax (local notes) surface; remote personal-space mode uses a scoped Agent token from the web UI. |

Gateway source maintenance (`yeisme-mcp-gateway-maintainer`), peering
(`yeisme-mcp-gateway-peer-operator`), and publishing
(`yeisme-mcp-gateway-provider`) keep their own triggers; this router never
replaces them.

## First-call verification discipline (all surfaces)

1. **Navigation maps are not truth.** Each operating skill embeds a map plus a
   `card` script or official discovery call. Confirm names once per session
   against the live surface before the first execute:
   - eikona: `eikona-mcp-actions` `scripts/card.sh` (`eikona mcp capabilities
     --json --full`) or `GET /api/v1/mcp/actions`;
   - scaena: one `tools/list`, then `scaena.search` and readable owner resources;
     `scaena mcp capabilities --json` is optional when the CLI is installed;
   - auctra: `auctra mcp capabilities --json` then read the
     `auctra://authoring/capabilities` resource; planned actions are
     listed for honesty and are not executable;
   - sonora: `sonora mcp capabilities --json` or `sonora.search` with
     `types:["command"]`;
   - anatomia: `anatomia mcp doctor --json` then `anatomia mcp capabilities --json`;
   - drivebridge: `drivebridge doctor` (read-only preflight) then
     `drivebridge capabilities --json` or the `drivebridge://capabilities`
     resource; `not_probed` statuses are honest, not failures;
   - gateway backends: one `tools/list` (compact; full schema per tool via
     `GET /v1/tools/{name}` only when needed);
   - gitea-mcp: the catalog `search` itself is discovery — never skip it.
2. **Never guess or pluralize tool/action names.** A typed
   `UNKNOWN_ACTION`/`-32602`-family error means re-discover, not try-again.
3. **Denials are opaque by design.** Unknown and non-entitled actions return
   identical errors (existence-oracle protection). On denial, reassess the
   lane/principal; do not probe names.
4. **Digest drift.** Card scripts emit `digest_sha256_16` + `generated_utc`;
   if a typed error contradicts the map, re-run the card and compare.
5. **One discovery, then commit.** Batch exploration (`search` once with good
   terms, `limit` bounded) beats iterated probing; every skill's shortest
   sequence is written to finish common jobs in 2-3 calls.

## File input without a product CLI

When the task needs a client file, first inspect the connected owner's `://input/capabilities` resource and `tools/list` schemas. Use its advertised typed tools or execute action mapping; never require local CLI help to discover an already connected MCP contract. CLI discovery remains optional when that product CLI is installed. Unconfigured, readonly or older deployments do not gain planned actions.

If the host can read the selected file and send HTTP, prepare the original input request with its stable idempotency key, consume the transient grant link in memory and stream bytes to the issuing owner. For an unknown file, omit metadata and enter awaiting_file. A pure MCP host gives the user the one-time page link, then polls the same input request. One request binds one file; use multiple requests for multiple references.

Keep grants/page URLs out of normal receipts, logs, notes and persisted tool bodies. Never use redacted placeholders or guess URLs. If Gateway reports INPUT_LINK_RELAY_UNAVAILABLE, recover the original request through a host preserving transient resource links. On interruption, query the original ID (or reuse the identical prepare key to retrieve its ID) before renew/cancel/retry. This input-only recovery rule does not authorize resubmitting a generation request.

Return only the stable owner input reference to the original task. Upload completion does not approve generation, analysis, canonical acceptance, overwrite or payment. Eikona, Scaena, Sonora, Anatomia, Auctra, Pinax and Radar have separate owner gates; Ordo input upload is deferred by the user. Deployment and installed capabilities must be checked independently of source-level availability.
