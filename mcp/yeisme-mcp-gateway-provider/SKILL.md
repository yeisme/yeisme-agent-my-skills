---
name: yeisme-mcp-gateway-provider
description: Use when an MCP service owner needs to publish explicitly authorized tools, resources, or prompts through a Yeisme MCP Gateway, create export-profile-bound consumer credentials, or hand off a provider endpoint without exposing Gateway management authority.
---

# Yeisme MCP Gateway Provider

Publish an existing MCP service through the Gateway's single `/mcp` endpoint.
Do not create Pack-specific endpoints, give consumers upstream credentials, or
grant management scopes to service consumers.

## Inputs

Establish the base Registry backend, public capability names, tenant/workspace,
export profile id, budget and approval policy, TTL/call limits, credential sink,
and intended consumer. Backend credentials stay in local secret storage and
enter managed configuration only as `env://` or permission-checked absolute
`file:///` references.

## Publication workflow

1. Validate the base backend and explicit exposure through the normal Registry
   workflow.
2. Inspect the active revision and the `sharing.export_profile.upsert` Action.
3. Plan an export profile listing exact public tools/resources/prompts.
4. Apply the approved plan and retain its revision and operation receipt.
5. Create a service token bound to tenant, workspace, and export profile; write
   it directly to an approved local credential sink.
6. Hand off only the Gateway `/mcp` URL and credential reference.

Configure a scoped delegated credential before using the CLI examples:

```bash
export MCP_GATEWAY_ADMIN_ENDPOINT=https://gateway.example.com
export MCP_GATEWAY_TOKEN_FILE=/absolute/path/provider-agent.token
```

```bash
mcp-gateway config revisions --json
mcp-gateway admin inspect action sharing.export_profile.upsert --json
mcp-gateway admin plan sharing.export_profile.upsert \
  --expected-revision cfgrev_xxx \
  --input-json '{"profile":{"schema":"gateway_export_profile.v1beta1","id":"partner-read","tenant_id":"acme","workspace_id":"platform","tools":["docs_search"],"resources":[],"prompts":[],"ttl_seconds":86400,"max_calls":1000,"enabled":true}}' \
  --json
mcp-gateway admin apply plan_xxx --plan-digest sha256:xxx --approval-id appr_xxx --json
```

Create the credential through the Action Catalog; the response returns metadata
and the credential reference, never the plaintext token:

```bash
mcp-gateway admin plan token.create \
  --expected-revision cfgrev_xxx \
  --set tenant_id=acme \
  --set workspace_id=platform \
  --set actor_type=service_account \
  --set actor_id=partner-consumer \
  --set scopes='["mcp:discover","mcp:tools:read","mcp:tools:call"]' \
  --set export_profile_id=partner-read \
  --set credential_sink_ref=file:///secure/partner-consumer.token \
  --json
```

Apply both high-risk plans with their returned `plan_digest` and bound
`approval_id`. Do not reuse approval evidence across plans or revisions.

## Provider Pack

Use the built-in starting template when distribution is useful:

```bash
mcp-gateway pack init ./packs/provider-publish \
  --template provider-publish \
  --version 0.1.0
mcp-gateway pack validate ./packs/provider-publish --json
```

The Pack may describe Registry overlays, export profiles, parameters, client
instructions, and local Skill name/version references. It must not include
secrets, scripts, hooks, binaries, remote Skill content, or install commands.

## Verification and handoff

Verify that a consumer token sees exactly the profile capabilities, cannot see
admin tools, expires within the profile TTL, stops at `max_calls`, and remains
revocable. Report the provider Gateway identity, `/mcp` endpoint, export profile
id, revision, operation/receipt ids, credential reference, capability list, and
redacted evidence path.

Use `yeisme-mcp-gateway-maintainer` for code changes and
`yeisme-mcp-gateway-operator` for general administration.
