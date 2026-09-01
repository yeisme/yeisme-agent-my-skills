---
name: yeisme-mcp-gateway-peer-operator
description: Use when a Gateway owner needs to create, approve, probe, inspect, disable, or remove a one-way trusted Gateway peer, including identity/digest pinning, namespace conflicts, loop or hop rejection, degraded-cache handling, and non-re-export guarantees.
---

# Yeisme MCP Gateway Peer Operator

Operate one-way, one-hop Gateway peering. A Streamable HTTP MCP backend without
modern `server/discover` can remain a normal backend, but it does not receive
peer identity, namespace, or failure-isolation semantics.

## Establish trust inputs

Collect the local Gateway instance id, remote `/mcp` HTTPS endpoint, local
`auth_ref`, deterministic namespace, expected remote server id, active revision,
and approval owner. Never resolve or print the peer credential. Each direction
requires its own peer record; a reverse connection is not implied.

Peer topology changes are local-owner Actions in V1. Configure the local
break-glass endpoint and credential before using the commands:

```bash
export MCP_GATEWAY_ADMIN_ENDPOINT=https://local-gateway.example.com
export MCP_GATEWAY_ADMIN_TOKEN_FILE=/absolute/path/admin.token
```

## Plan and probe

```bash
mcp-gateway peer plan add partner \
  --endpoint https://partner.example.com/mcp \
  --auth-ref file:///secure/partner.token \
  --namespace partner \
  --expected-server-id partner-gateway \
  --json
mcp-gateway peer apply plan_xxx --plan-digest sha256:xxx --approval-id appr_xxx --json
mcp-gateway peer probe partner --json
mcp-gateway peer show partner --json
```

The first successful probe pins the remote instance identity and semantic
discovery digest. Identity or digest drift moves the peer to blocked until a new
plan is reviewed and approved. Do not silently accept drift or overwrite the
pinned values.

## Invariants

- Imported capabilities carry `origin_gateway_id`, `peer_id`, and `hop=1`.
- Gateway-generated HTTP `Via` and MCP `_meta["yeisme.gateway.peer"]` must agree.
- Self identity, repeated origin, duplicate chain entries, hop greater than one,
  and attempts to re-export imported capabilities are rejected.
- `gateway_peer` credentials have discovery/read/call scopes only and never
  inherit management scopes.
- Namespace collisions are plan-time errors; do not rename implicitly.
- A peer outage degrades only its namespace. A bounded last-known discovery
  cache may be used until its expiry; uncertain writes are not replayed.

## Recovery

For an expected maintenance outage, preserve the peer record and diagnose the
namespace. For identity drift, self-loop, repeated origin, or hop failure, stop
and require a new approval. Disable or remove through revision-safe plans:

```bash
mcp-gateway peer plan disable partner --json
mcp-gateway peer apply plan_xxx --plan-digest sha256:xxx --json
mcp-gateway peer plan remove partner --json
```

Report peer id, namespace, expected/observed identity, discovery digest, status,
cache expiry, revision, operation id, failure class, and the exact next safe
command. Do not expose `auth_ref` contents.

Use `yeisme-mcp-gateway-consumer` for ordinary capability calls and
`yeisme-mcp-gateway-maintainer` for source changes.
