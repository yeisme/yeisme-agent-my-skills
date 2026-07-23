---
name: yeisme-taskbridge-cli-runtime
description: Compatibility alias for yeisme-connectors-task-runtime during the TaskBridge-to-Connectors skill migration; use when older routing still names the TaskBridge runtime skill.
---

# Yeisme TaskBridge CLI Runtime

This published name is retained for one compatibility release. Route all new work to `yeisme-connectors-task-runtime`, whose owner is `backend-server/connectors` and whose primary command surface is `connectors task`.

Do not add new profile assignments for this alias. Existing assignments must migrate to `yeisme-connectors-task-runtime` before the alias is removed in a later breaking skill release.

Validation and maintenance commands are defined by the replacement skill.
