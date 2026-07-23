# Connectors Task Runtime Maintenance

## Compatibility lanes

- Formal entrypoint: `connectors task ...`.
- Compatibility entrypoint: `taskbridge ...`, built from `backend-server/connectors/cmd/taskbridge`.
- Stable compatibility schemas: `taskbridge.agent-result.v1`, `taskbridge.today.v1`, `taskbridge.actions.v1`, `taskbridge.action-result.v1`, `taskbridge.action-audit.v1`, and `taskbridge.rpc-result.v1`.
- Removal status owner: `internal/taskcompat`.

## Release evidence

Run `scripts/taskbridge-replacement-smoke.sh`. The runner builds both binaries, validates version and agent schema commands, exercises migration/rollback tests, scans persisted output, and writes a system evidence bundle under `temp/integration-test-runs/`.

Do not mark the replacement release ready until root installation scripts build both binaries from Connectors, Pinax prefers Connectors, repository references no longer require the old subproject, and rollback remains rehearsed.
