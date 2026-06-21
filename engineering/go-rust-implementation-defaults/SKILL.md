---
name: go-rust-implementation-defaults
description: Use when choosing whether a Yeisme capability should stay in TypeScript/Bun, consume a prebuilt native package, or escalate to Go/Rust for backend/CLI/MCP/daemon/worker/system components.
---

# Go/Rust Implementation Defaults

Use this skill when a Yeisme task involves language choice, backend architecture, CLI architecture, MCP servers, daemons, workers, process/filesystem/system capabilities, or a proposal to move a TypeScript/Bun tool into Go/Rust/native code.

## Default Policy

Yeisme projects should not default to language migration. Start from the project's main language, then escalate only when the capability needs it.
> A language or module-path migration is a generation-breaking change even when behavior is preserved. Follow `yeisme-evolutionary-change-policy`: gate it behind an OpenSpec change with a dual-run transition, consumer migration, deprecation window, and rollback before moving a capability across languages or changing a Go module / TS package path.

- Prefer **TypeScript/Bun** for Cohors, agent/team tools, provider orchestration, plugin SDKs, typed clients, output renderers, TUI glue, and fast control-plane iteration.
- Prefer **Go** for separate backend services, MCP servers, gateways, daemons, workers, long-running processes, sync tools, HTTP/SSE servers, health checks, resource control, and operational tooling when a service/process boundary is clear.
- Prefer **Rust** for native/system kernels only when the project owns or patches that native layer: parser-heavy code, codecs, filesystem primitives, memory-sensitive hot paths, high-performance hashing/diff kernels, WASM/native libraries, or maintained Rust crates.
- Prefer **prebuilt native packages** over local Rust development when a maintained package already exposes the needed native binding to TypeScript/Bun.
- Use **Python** mainly for data experiments, offline scripts, and eval glue, not default long-running backend services.

For Go subprojects, default to **pure Go**. Backend services, MCP/gateway services, daemons, workers, synchronizers, and single-binary CLIs should keep normal build/test/release paths compatible with `CGO_ENABLED=0`. Do not introduce cgo for broad performance claims; the added debugging, cross-compilation, deployment, and release cost is not justified for ordinary Yeisme high-concurrency services or monolithic CLIs.

## Cohors Rule

Cohors specifically should be designed as:

```text
TypeScript / Bun mainline
  CLI UX, Pi projection, provider/protocol adapters, config, plugins, TUI glue

Optional Pi native package integration
  @oh-my-pi/pi-natives or packages/natives exposes native binding to TS/Bun

Pi / OMP dependency ownership
  consume released npm packages by default; use fixed Git refs only as short-lived bridges; fork and publish a scoped package only for maintained native/runtime differences; do not default to source submodules inside cli/cohors

Go
  not the default Cohors native layer; use Go for separate services only when that process boundary is explicitly better than a native package

Rust
  upstream package implementation detail; enter Rust only to fork, patch, or contribute the native package
```

For Cohors details, follow `cli/cohors/docs/design/pi-native-package-integration.md`.

## Decision Checklist

Before moving a TypeScript/Bun tool capability to Go/Rust/native code, check:

- Is this long-running or resource-sensitive?
- Does it manage processes, PTY, filesystem, sandbox, sockets, or concurrency?
- Does it need a single cross-platform binary?
- Does it expose MCP, HTTP/SSE, daemon, worker, or gateway behavior?
- Does it need race tests, signal handling, health checks, and operational observability?
- Is there measured startup, latency, throughput, memory, or correctness evidence showing TS/Bun is insufficient?

If no, keep the capability in TypeScript/Bun or the current project language.

If yes and this is a separate service/process boundary, evaluate Go first.

Before choosing cgo in a Go project, check:

- Is there a pure-Go package, standard-library approach, external process boundary, or existing service integration that solves the requirement?
- Is the requirement a true platform/system binding, legacy compatibility bridge, or measured correctness constraint rather than a generic performance claim?
- Can the cgo dependency be isolated behind a narrow adapter without leaking into business logic, CLI output, protocol handling, repositories, or service APIs?
- Have debugging, cross-compilation, release, container, CI, and operations impacts been documented in the owning OpenSpec design?
- Does the design preserve a `CGO_ENABLED=0` default build or provide a clear fallback/rollback when that is impossible?

If any answer is no, stay pure Go.

Before choosing local Rust, check:

- Is this a native binding, parser, AST, shell, isolation, filesystem, hashline, codec, or WASM/kernel boundary?
- Is there an existing package such as `@oh-my-pi/pi-natives` that already exposes the capability to TypeScript/Bun?
- Are you actually forking, patching, or upstreaming that package, and will the result be consumed as a versioned package instead of a default Cohors source submodule?
- Is release/prebuild/cross-platform complexity acceptable?
- Is Rust isolated to a small kernel instead of owning product policy?

If the answer is no and the component is a Cohors feature, keep it in TypeScript/Bun. For Cohors native/system capabilities, choose the existing native package first; do not create local Rust crates by default.

## Cohors Pi / OMP Dependency Modes

For Cohors dependencies on Pi / OMP runtime capabilities:

- **Default:** consume released packages such as `@oh-my-pi/pi-natives` and `@oh-my-pi/pi-tui` through TypeScript facades, lazy loading, capability projection, and fallback states.
- **Temporary:** use a fixed Git ref or package patch only when waiting for an upstream release. Record the commit, reason, risk, and return-to-release plan.
- **Long-term divergence:** fork upstream only when Cohors must maintain native/runtime changes. Publish the fork as a scoped package and keep upstream sync, license, prebuild CI, fallback, and rollback documented.
- **Avoid:** do not add `earendil-works/pi`, `oh-my-pi`, or similar Pi / OMP source repositories as default `cli/cohors` submodules. Submodules are only acceptable after a design explicitly proves package or forked-package consumption cannot work.

When reviewing a Cohors plan, treat a request to add a Pi / OMP source submodule as a design smell unless the plan includes native source ownership, build reproducibility, security/license audit, cross-platform CI, and a removal path.

## Documentation Requirements

When documenting the decision:

- Name the owner language for each layer.
- State why TS is or is not enough.
- State why Go or Rust is selected.
- For Go projects, state how the normal path stays pure Go and `CGO_ENABLED=0`; if cgo is unavoidable, document the exception evidence, adapter boundary, and fallback/rollback.
- Include fallback behavior and resource budgets.
- For Cohors Pi / OMP dependencies, state whether the dependency mode is released package, temporary Git ref/patch, forked scoped package, or exceptional submodule, and explain the exit path.
- Include real validation commands.

Reference doc: `docs/architecture/language-runtime-strategy.md`.

## Guardrails

- Do not put UI rendering, localized CLI text, approval policy, provider prompt policy, or product state machine into Rust by default.
- Do not move Cohors features out of TypeScript/Bun without measured performance, system, or distribution evidence.
- Do not choose local Rust just because another project uses Rust; require ownership of a native package, a system API reason, or an explicit fork/patch/upstream plan.
- Do not add cgo to Go backends, MCP/gateway services, daemons, workers, synchronizers, or single-binary CLIs for generic performance claims.
- Do not let cgo become a transitive default release requirement without OpenSpec evidence, an isolated adapter, and deployment/debugging impact notes.
- Do not choose Go-only for Cohors; Cohors still needs TS/Bun for CLI/control-plane and AI ecosystem integration.
- Do not default Cohors native/system capabilities to local Rust or a Go sidecar when `@oh-my-pi/pi-natives` can be consumed as a package.
- Do not default Cohors Pi / OMP integration to Git submodules or vendored upstream source. Prefer package consumption; fork only when maintaining a native/runtime difference.
