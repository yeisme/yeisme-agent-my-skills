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
| scaena mcp operations | *(pending)* | Operating skill lands with the scaena owner wave; until then use `scaena mcp` docs in `agent/scaena` and the same verification discipline |

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
