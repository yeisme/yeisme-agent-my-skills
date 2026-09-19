# Commands

HTTP only. Schema: `anatomia.vlm_codex_interaction.v1`. Use the Go SDK in `agent/anatomia/sdk/client` when calling from owner code.

```
GET  /api/v1/interactions/{session_ref}
GET  /api/v1/interactions/{session_ref}/events?cursor=&limit=
POST /api/v1/interactions/{session_ref}/cancel
POST /api/v1/interactions/{session_ref}/attempts/{attempt_ref}/reconcile
GET  /api/v1/interaction-routes/{route_decision_ref}
POST /api/v1/interaction-routes/{route_decision_ref}/attempts/{provider_attempt_ref}/reconcile
```

Reconcile classifies the original attempt receipt. It does not start a new turn or a paid Provider attempt.

## Planned / do not run

```
anatomia video dialogue *
anatomia skills list   # hides this skill unless --all
```

Do not invent CLI verbs to wrap these HTTP routes.
