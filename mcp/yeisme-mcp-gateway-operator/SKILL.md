---
name: yeisme-mcp-gateway-operator
description: Use when an owner or delegated Agent needs to inspect or operate a deployed Yeisme MCP Gateway through its CLI, scoped admin API, or five admin MCP tools, including revision-safe changes, approvals, Packs, credentials, and rollback without changing Gateway source code.
---

# Yeisme MCP Gateway Operator

Operate an existing Gateway through its versioned Action Catalog. The Gateway,
not the client, derives `local-owner` or `delegated-agent` from the authenticated
principal. Never ask a caller to declare an admin profile in request input.

## Establish the boundary

Identify the admin endpoint, credential source, tenant/workspace, active
revision, intended Action, and whether an approval is required. Keep the static
admin token as a local-owner break-glass path; ordinary remote Agents use scoped
credentials. Do not print tokens, resolved secrets, raw Authorization headers,
or sensitive action payloads.

Preview features must be explicitly enabled at service startup:

```bash
mcp-gateway serve --registry ./registry.yaml \
  --enable-admin-mcp \
  --enable-gateway-packs \
  --enable-gateway-peering
```

Bootstrap-only settings—listen address, TLS identity, data directory, owner
trust, admin-token source, and secret resolvers—remain local configuration and
must not be changed through admin Actions.

For CLI administration, configure the endpoint and exactly one credential
file. Delegated Agents use `MCP_GATEWAY_TOKEN_FILE`; local-owner break-glass
uses `MCP_GATEWAY_ADMIN_TOKEN_FILE`:

```bash
export MCP_GATEWAY_ADMIN_ENDPOINT=https://gateway.example.com
export MCP_GATEWAY_TOKEN_FILE=/absolute/path/delegated-agent.token
```

## Inspect before mutation

```bash
mcp-gateway admin inspect gateway --json
mcp-gateway config revisions --json
mcp-gateway admin search --kind action --query registry --agent
mcp-gateway admin inspect action registry.backend.disable --json
```

Use `gateway_admin_search`, `gateway_admin_inspect`,
`gateway_admin_operations`, `gateway_admin_plan`, and `gateway_admin_apply`
when operating through MCP. These tools expose catalog Actions only; they are
not an arbitrary HTTP method/path proxy.

## Plan, approve, apply

Every mutation is revision-bound and idempotent:

```bash
mcp-gateway admin plan registry.backend.disable \
  --backend gitea \
  --expected-revision cfgrev_xxx \
  --json

mcp-gateway admin apply plan_xxx \
  --plan-digest sha256:xxx \
  --approval-id appr_xxx \
  --json

mcp-gateway admin operations --watch op_xxx --events
```

On a CAS conflict, inspect the new active revision and create a new plan; do not
auto-merge. An approval is valid only for its plan digest, revision, principal,
and expiry. Reusing an idempotency key with a different payload is an error.

## Packs and rollback

Packs are declarative, immutable, signed artifacts. They may reference local
Skill names and versions but never install or carry Skill content.

```bash
mcp-gateway pack templates --json
mcp-gateway pack validate ./packs/team-shared --json
mcp-gateway pack fetch https://example.com/packs/team-shared/0.1.0/pack.json \
  --digest sha256:xxx \
  --json
mcp-gateway pack plan pack:team-shared@0.1.0 \
  --expected-revision cfgrev_xxx \
  --json
mcp-gateway admin apply plan_xxx --plan-digest sha256:xxx --approval-id appr_xxx --json
```

Do not follow `latest`, auto-upgrade, accept executable fields, or enable
unsigned artifacts outside explicit loopback development mode. Publisher trust
is local-owner bootstrap state.

Rollback creates a new revision; it never rewrites history:

```bash
mcp-gateway config rollback cfgrev_previous \
  --expected-revision cfgrev_current \
  --json
```

## Boundaries and handoff

- Use `yeisme-mcp-gateway-maintainer` for source changes.
- Use `yeisme-mcp-registry-onboarding` for base Registry authoring.
- Use `yeisme-mcp-gateway-provider` for service publication and export grants.
- Use `yeisme-mcp-gateway-peer-operator` for peer identity, hop, and namespace operations.
- There is no full management Web UI, TUI, Marketplace, anonymous access,
  recursive federation, or dynamic Skill installation in V1.

Return the active revision, Action/plan/operation ids, approval state, result or
rollback revision, redacted evidence path, and the exact safe next command.

## References

- `mcp/gateway/docs/remote-admin.md`
- `mcp/gateway/docs/auth.md`
- `mcp/gateway/README.md`
