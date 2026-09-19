## UI Spec Minimum Shape

Use this shape when no project-specific template exists:

```yaml
page:
  name: Example Page
  route: /example
  viewports:
    desktop: 1440x960
    mobile: 390x844

design_tokens:
  product_posture:
    type: engineering-tool
    keywords: [high-density, calm, professional, low-saturation, non-marketing]
  typography:
    family: Inter or existing project font
    mono_family: existing mono font
    base_size: 14
  spacing:
    scale: [4, 8, 12, 16, 24, 32]
  radius:
    default: 8
    card: 8
    button: 8
  color:
    allowed_semantic_tokens: [background, foreground, muted, muted-foreground, card, border, primary, success, warning, destructive, info, chart-1, chart-2, chart-3, chart-4, chart-5]
    source: CSS variables or existing theme tokens
  motion:
    duration_fast: 120ms
    duration_normal: 180ms
    duration_slow: 240ms
    easing_standard: ease-out
    easing_emphasized: cubic-bezier(0.16, 1, 0.3, 1)

layout:
  shell: app shell or page frame
  page_pattern: table-inspector
  regions:
    - id: sidebar
      width: 240
      responsive: collapses below tablet
    - id: statusbar
      height: 56
      responsive: remains visible, condenses secondary metadata
    - id: main
      width: fluid
      grid: 12 columns on desktop when useful
    - id: inspector
      width: 360
      responsive: drawer on mobile

components:
  approved_libraries: [existing project components, shadcn/ui new-york, Radix, Tailwind CSS 4, lucide-react, React Router 7, TanStack Query 5, TanStack Table 8, React Hook Form, Zod, sonner, Recharts, cmdk, existing approved motion capability, Playwright, MSW]
  repeated:
    - name: TaskCard
      source: existing component or new component
      states: [default, hover, selected, active, disabled, loading, error, empty]
      props: [title, status, progress]

interactive_controls:
  - id: run-filter-select
    primitive: Select or Combobox from approved component library
    purpose: filter runs by status
    states: [closed, open, hover, focus, selected, disabled, loading, empty]
    keyboard: [Tab focuses trigger, Enter or Space opens, Arrow keys move, Enter selects, Escape closes]
    data: status options from API or local enum
    acceptance: open menu is aligned, scrollable if long, selected value persists, no off-token styling
  - id: artifact-preview
    primitive: Dialog or Sheet with image viewer
    purpose: preview clicked image artifact
    states: [closed, open, loading, loaded, error]
    keyboard: [Enter opens from thumbnail, Escape closes, Tab traps focus, Arrow keys navigate when gallery exists]
    acceptance: image preserves aspect ratio, supports zoom or open-original action when useful, background scroll is locked

blacklist:
  - broad blue-purple gradients
  - glassmorphism cards
  - excessive shadows
  - random emoji as icons
  - card-heavy layouts without real data density
  - icon on every module without semantic need
  - oversized hero sections for product tools
  - landing-page style composition for dashboards
  - meaningless metric cards
  - all-centered layouts for operational tools
  - more than five competing semantic colors

acceptance:
  - Screenshot matches target structure, density, and spacing at fixed viewports.
  - No text overlap or layout shift during loading, empty, or error states.
  - Motion is subtle, supports reduced motion, and never changes the intended layout structure.
  - Implementation uses only approved tokens and component families.
  - Page follows the selected pattern and exposes a clear recommended next action.
  - Every visible interactive control is implemented, keyboard reachable, styled through the same component system, and covered by a story or Playwright interaction check when practical.
```

