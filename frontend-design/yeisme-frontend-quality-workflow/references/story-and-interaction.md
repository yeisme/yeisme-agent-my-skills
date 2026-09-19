# Story coverage and interaction checks

For AI-generated UI, default stories should include:

- `Default`
- `Loading`
- `Empty`
- `Error`
- `DenseData`
- `Selected`
- `Open`
- `Disabled`
- `KeyboardFocused`
- `Mobile`
- `DarkMode` when the app supports dark mode

For page-level stories, represent the selected pattern explicitly, for example:

- `DashboardOverview`
- `ListDetail`
- `TableInspector`
- `TimelineEventDetail`
- `ApprovalQueue`
- `ArtifactBrowser`
- `Diagnostics`
- `SettingsControl`
- `CostUsage`
- `EmptyOnboarding`

When these controls are touched, add a Storybook story, Playwright interaction check, or documented manual fallback:

| Control | Required Checks |
| --- | --- |
| Select / Combobox | opens, keyboard selects, empty/loading option, selected value persists |
| Dropdown / Context menu | trigger alignment, disabled item, action fires or is intentionally stubbed, Escape closes |
| Dialog / AlertDialog | focus trap, title/description, Escape or explicit close, destructive confirmation |
| Popover / HoverCard | anchored position, outside click behavior, focus return |
| Sheet / Drawer | mobile behavior, scroll lock, close affordance |
| Image / Artifact preview | thumbnail click, loading, error, aspect ratio, close, optional next/previous |
| Table controls | sort, filter, pagination, row selection, dense data, empty data |
| Forms | labels, validation, submit loading, server error, disabled/save states |
| Toast / Alert | semantic styling, dismiss policy, retry or next action where useful |
| Command palette | open shortcut or trigger, search, no results, keyboard navigation |

TypeScript Web/Node test layering:

- `unit`: Vitest for pure functions, single objects, and complex rules
- `integration`: Vitest for service/repository, component/store/API mock, or API handler + app harness
- `component`: one complete frontend page or backend service component with real or controlled dependencies and mocked external boundaries
- `system`: multiple services started together for system-level behavior
- `e2e`: user or automation entry through the full business chain; browser paths use Playwright, CLI/API paths do not require a browser

Default stack unless the project already has an equivalent: Vitest; Testing Library + MSW for frontend component/page integration; Supertest, Fastify `inject()`, or framework injection for backend HTTP/API; Testcontainers or the project's docker compose/test harness for real dependencies; Playwright for a small number of critical browser E2E paths.
