---
name: remotion-animation-workflow
description: Use when designing, implementing, or reviewing React-based rendered animations and video artifacts with Remotion, including product walkthroughs, data-driven clips, reusable compositions, in-app previews with @remotion/player, or server-side rendering integration; do not use for ordinary webpage microinteractions.
---

# Remotion Animation Workflow

Use Remotion when the deliverable is a timeline-based artifact that must preview consistently and render to video or still output. Keep ordinary button, menu, route, layout, and feedback motion in the frontend stack with CSS, Web Animations, or the project's existing motion library.

## Inputs

Collect:

- artifact purpose, audience, aspect ratio, duration, fps, and output format
- storyboard or scene list, copy, data inputs, media assets, fonts, audio, and captions
- whether the product needs Studio authoring, an embedded `<Player>`, rendered files, or all three
- existing package manager, React version, deployment target, and rendering environment
- accessibility, reduced-motion, rights, privacy, budget, and evidence requirements

## Route The Work

Choose one path:

| Need | Route |
| --- | --- |
| Web UI microinteraction | Keep it in the frontend project; do not add Remotion |
| Standalone authored video | Remotion composition + Studio + CLI render |
| Product walkthrough or data-driven clip | Parametric composition + typed props + render command |
| In-app interactive preview | Shared composition + `@remotion/player` adapter |
| User-triggered downloadable video | Player preview + authenticated server render boundary |
| High-volume or cloud rendering | Separate rendering service or approved Remotion cloud runtime |

If the admitted official `remotion-best-practices` skill is available, load it after this workflow as the Remotion domain reference. Keep this skill responsible for Yeisme routing, architecture, permissions, evidence, and project boundaries.

## Integrate An Existing Project

1. Read the owning project's `AGENTS.md`, package manager lockfile, frontend architecture, design system, and test commands.
2. Confirm the organization is eligible under the current Remotion License or has the required Company License before adding a production dependency.
3. Keep all Remotion packages on the same exact version. Do not use mismatched versions or caret ranges. Use the project's package manager and `remotion add` for optional packages.
4. Isolate compositions from application screens, data fetching, credentials, and product state machines.
5. Define typed input props and Zod schemas at the composition boundary when users or automation supply parameters.
6. Reuse the same composition for Studio, `<Player>`, still checks, and final rendering instead of maintaining parallel preview markup.
7. Add rendering infrastructure only when output files are a required product capability. A browser preview alone does not justify server rendering.

For a standalone project, start from the official scaffold:

```bash
npx create-video@latest
```

For an existing application, follow the official brownfield installation guide before adding packages. Examples for optional packages:

```bash
npx remotion add @remotion/player
bunx remotion add @remotion/player
pnpm exec remotion add @remotion/player
yarn remotion add @remotion/player
```

Run only the command matching the project's existing package manager.

## Composition Contract

Keep a stable structure such as:

```text
src/remotion/
  Root.tsx
  compositions/
  scenes/
  components/
  schemas/
  assets/
  render/
```

Require:

- frame-based timing from `useCurrentFrame()` and `useVideoConfig()`
- deterministic output for the same props, assets, fps, dimensions, and version
- explicit scene durations and transitions instead of incidental CSS timing
- `staticFile()` or approved remote asset loading with render-safe readiness handling
- measured text and overflow handling for dynamic copy
- stable IDs, default props, metadata calculation, and schema validation for compositions
- no secrets, Authorization headers, raw prompts, provider payloads, or private URLs in composition props or render logs

## Frontend Boundary

When embedding `<Player>`:

- keep product authorization, data loading, mutations, and receipts outside the composition
- pass a redacted immutable projection into the Player
- disable autoplay or heavy preview behavior when reduced motion, device limits, or visibility state requires it
- provide accessible controls, labels, keyboard behavior, loading, error, and unavailable states
- lazy-load the Player when it is not part of the primary interaction path
- keep rendered output semantics separate from responsive page layout; the composition owns a fixed canvas

## Rendering Boundary

Treat rendering as a privileged backend capability:

- authenticate and authorize render requests
- validate composition ID, props, asset references, dimensions, duration, codec, and output location
- apply idempotency, concurrency limits, rate limits, timeouts, cancellation, cost controls, and cleanup
- keep browser binaries, renderer packages, cloud credentials, and object-storage writes outside the frontend bundle
- assume `REMOTION_*` variables and `.env` values can reach the headless browser; never place secrets there unless the official security guidance explicitly permits the exposure
- return job state, progress, artifact references, errors, and redacted receipts through the owning service contract
- preserve integration-test evidence under the owning subproject's `temp/integration-test-runs/<run-id>/`

Do not let React pages call Remotion Lambda, renderer internals, provider SDKs, or object storage directly.

## Verification

Start narrow and expand:

```bash
npx remotion studio
npx remotion versions
npx remotion still <composition-id> --frame=0
npx remotion render <composition-id> out/<composition-id>.mp4
```

Also run the owning project's typecheck, lint, unit tests, build, and browser tests. Verify representative frames at scene boundaries, the final frame, long text, missing media, alternate aspect ratios, caption timing, audio levels, reduced-motion preview behavior, and render failure recovery.

## Boundaries

- Do not add Remotion to every frontend project by default.
- Do not use Remotion to replace ordinary UI animation libraries.
- Do not introduce cloud rendering, Lambda, Vercel Sandbox, Cloudflare Containers, or a render server without an accepted architecture and operations plan.
- Do not claim deterministic output without rendering at least one still or short artifact from the real composition.
- Do not vendor external skill sources without a reviewed license and pinned source.
- Use `references/official-sources.md` for the reviewed official entry points and source status.
