## Backend Service Logging Contract

Every backend service, worker, daemon, MCP server, agent runtime service, and long-running `serve`, `watch`, scheduler, or bridge mode must be debuggable without reading source code or attaching a debugger.

Do not accept services that only print `localhost:<port>`, `server started`, or other free-form status lines. Startup output must identify what is running, where diagnostics go, how calls are correlated, and whether dependencies are ready.

Required logging behavior:

- Default to structured JSON logs for every service and daemon, including HTTP APIs, workers, schedulers, browser bridges, MCP servers, and long-running CLI `serve`/`watch` modes. Text logs are allowed only for explicitly human-only CLI summaries, never for service diagnostics.
- Keep machine/protocol stdout clean. HTTP services must not rely on stdout banners or `fmt.Println` status lines for diagnostics; stdio MCP/protocol services must reserve stdout for protocol frames only.
- Every service runtime must have an explicit diagnostic sink policy: stderr for foreground development, protocol-safe stderr for stdio-compatible services, plus a configured rotating file sink for local/dev debugging unless the owning platform explicitly forbids local files.
- File sinks must be bounded and rotated by size and/or age with retention. Never append forever to one unbounded log file.
- Include correlation fields on every relevant line: `service`, `component`, `event`, `request_id`, `trace_id`, `run_id`, `task_id`, `worker_id`, `call_id`, `operation`, `target`, `status`, `duration_ms`, and `error_code` where applicable.
- Log lifecycle events: config loaded, service starting, bind/listen address, service ready, dependency readiness, shutdown requested, shutdown complete, and fatal startup failure.
- Log call lifecycle around external and internal boundaries: call started, call completed, call failed, retry scheduled, retry exhausted, timeout, cancellation, and circuit/rate-limit decisions.
- For tool, LLM, browser, Firecrawl, database, queue, or subprocess calls, include dependency name, sanitized target/resource id, attempt, timeout, result count/bytes, and duration. Do not log full prompts, scraped page text, provider payloads, tool outputs, tokens, cookies, auth headers, or connection strings.
- Use stable event names such as `service.starting`, `service.ready`, `http.request.completed`, `worker.job.started`, `call.started`, `call.completed`, `call.failed`, `dependency.ready`, and `shutdown.completed`.
- Make log level configurable through the owning project's config convention. `debug` and `trace` may add detail but must still redact secrets and truncate large values.

Recommended minimum JSON fields:

```json
{
  "ts": "2026-06-10T12:00:00Z",
  "level": "info",
  "service": "artifact-fetcher",
  "component": "firecrawl_client",
  "event": "call.completed",
  "request_id": "req_123",
  "trace_id": "trc_456",
  "run_id": "run_789",
  "call_id": "call_firecrawl_001",
  "operation": "fetch_markdown",
  "target": "https://example.com",
  "status": "ok",
  "duration_ms": 418,
  "attempt": 1,
  "result_bytes": 32768
}
```

For Go services, prefer `log/slog` with a JSON handler unless the subproject already owns an equivalent structured logger. Wrap logger construction once at process boundary; pass request-scoped loggers or fields through context deliberately, not via global mutable state.

Logging tests or smoke checks are required when adding or changing service startup, stdio/protocol mode, external calls, workers, or file logging:

- startup emits JSON logs with service name, bind address or stdio/worker mode, version/build where available, and log sink description
- stdio/protocol stdout contains only protocol data; diagnostics go to stderr or the configured rotating file
- call lifecycle logs include a stable `call_id`, status, duration, and sanitized target
- secret fields are redacted in stderr, rotating files, test snapshots, traces, and evidence
- file logging rotates or is explicitly bounded by size and/or age when enabled
- health/diagnostics smoke output points to logs by path or sink, not only to `localhost:<port>`

TraceEvent, audit records, and logs are separate artifacts. Logs diagnose runtime behavior; TraceEvent explains product/user-visible agent progress; audit records prove privileged decisions.

