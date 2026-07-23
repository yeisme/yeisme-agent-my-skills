---
name: lenis-smooth-scroll-integration
description: Use when adding, changing, testing, or reviewing Lenis smooth scrolling in a Web frontend, especially React/Vite applications with custom scroll containers, nested overlays, reduced-motion requirements, or an existing animation ticker.
---

# Lenis Smooth Scroll Integration

Integrate Lenis only where smoother scrolling improves the product. Preserve native scrolling semantics, accessibility, and the owning frontend's existing scroll architecture.

## Inspect First

Read the local `AGENTS.md`, package manifest, lockfile, frontend entrypoint, global CSS, scroll containers, overlays, browser tests, and animation/ticker setup.

Classify the target before installing:

| Scroll architecture | Default choice |
| --- | --- |
| Normal document scroll | One root Lenis instance may be appropriate |
| Fixed app shell with `body { overflow: hidden }` | Attach Lenis only to explicit content scrollers |
| Multiple panels, editors, dialogs, or drag surfaces | Opt in selected vertical content areas; keep controls native |
| Existing GSAP or shared RAF ticker | Disable Lenis auto RAF and drive one shared clock |

Reject the integration when native scrolling already meets the requirement or when the request is only decorative motion. Use `find-animation-opportunities` first when the product value of motion is unclear.

## Install

Use the owning project's package manager and pin the reviewed version when reproducibility matters. For a Bun project:

```bash
bun add lenis@1.3.25
```

Use the official package and CSS:

```ts
import Lenis from "lenis";
import "lenis/dist/lenis.css";
```

React projects may use `ReactLenis` from `lenis/react`, but a small lifecycle component around a custom scroll container is often clearer for panel-based applications.

## Implementation Contract

- Prefer `autoRaf: true` when Lenis owns its clock. Do not also call `lenis.raf()`.
- When an existing ticker owns the clock, set `autoRaf: false`, drive `lenis.raf(time)` from that ticker, and unregister it during cleanup.
- Call `destroy()` on unmount or option changes. React StrictMode must not leave duplicate listeners or RAF loops.
- Detect `prefers-reduced-motion: reduce` in the application. Do not create Lenis for those users; keep native overflow scrolling.
- Keep keyboard, focus, anchor, sticky, form-control, text-selection, and programmatic scrolling behavior usable.
- Do not enable `allowNestedScroll` by default. Prefer explicit scroller boundaries or `data-lenis-prevent`, `data-lenis-prevent-wheel`, and `data-lenis-prevent-touch` on nested native surfaces.
- Do not capture wheel or touch input used by dialogs, command palettes, editors, maps, carousels, horizontal tabs, drag handles, or resize handles.
- Enable `anchors` only when the product requires Lenis-managed anchor navigation and verify special-character targets.
- Use `lenis/snap` when scroll snap is required; do not assume native CSS scroll snap and Lenis will compose correctly.

## Verification

Use TDD for lifecycle or behavior changes. The focused test should prove:

- the intended wrapper/content elements receive the Lenis instance
- reduced motion leaves the scroller native
- unmount destroys the instance
- option changes do not create leaked instances

Then run the owning project's typecheck, unit tests, build, and browser checks. Browser acceptance should cover wheel, touch where available, keyboard scrolling, focus, nested overlays, mobile behavior, drag/resize interactions, and console errors.

For a Bun/Vite project, typical commands are:

```bash
bun run typecheck
bun test
bun run build
```

Document the exact integration scope, chosen RAF owner, reduced-motion fallback, excluded nested surfaces, verification commands, and removal command.

## Boundaries

- Do not install a second smooth-scroll library.
- Do not turn a fixed multi-panel application into document scrolling to simplify Lenis setup.
- Do not add GSAP, Motion, or a custom animation scheduler solely for Lenis.
- Do not claim a performance improvement without browser evidence.
- Do not use Lenis to hide layout jank, expensive rendering, or broken virtualization.
- Read [official-sources.md](references/official-sources.md) when choosing options, React integration, anchors, nested scrolling, or version compatibility.
