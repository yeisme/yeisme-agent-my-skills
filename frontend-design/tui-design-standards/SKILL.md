---
name: tui-design-standards
description: Use when designing, implementing, reviewing, or QAing terminal user interfaces, TUI dashboards, CLI interactive screens, Ink apps, Bubble Tea apps, curses-style interfaces, or terminal-first workflows; enforce mouse responsiveness and polished Apple-like visual quality.
---

# TUI Design Standards

Use this skill whenever the task touches a terminal UI: new TUI screens, TUI refactors, interactive CLI dashboards, keyboard shortcuts, terminal layouts, visual polish, or QA of terminal behavior.

## Core Rule

TUI is an interactive product surface, not formatted logs.

Every serious TUI must support mouse response unless the terminal framework or target runtime makes it impossible. If mouse support is impossible, say so explicitly, explain the technical blocker, and propose a concrete alternative. Do not silently ship keyboard-only interaction.

## Required Outcomes

- The user can operate primary workflows with mouse and keyboard.
- Clickable regions visibly look clickable before interaction.
- Mouse hover, click, scroll wheel, and selection states are intentionally designed.
- Routed detail panels restore the originating pane, selected row, prompt draft, cursor, and panel stack when closed.
- The interface feels refined, calm, rounded, and smooth: Apple-like, not boxy, noisy, or developer-tool raw.
- Visual hierarchy makes the current focus, selected item, active tab, and available actions obvious at a glance.

## Mouse Requirements

Treat these as acceptance criteria:

- **Tabs/nav**: click switches tabs or sections.
- **Rows/items**: click selects or opens the row that the cursor would select.
- **Buttons/actions**: click invokes the same command as the keyboard shortcut.
- **Scroll areas**: wheel scrolls lists and detail panes when content overflows.
- **Focus panes**: click changes focus between main and detail panes when applicable.
- **Hover**: hover gives a subtle affordance when the framework exposes mouse move events.
- **Disabled state**: disabled actions do not react except for optional explanatory status text.
- **No surprise exits**: mouse input must not quit, clear state, or trigger destructive behavior without an explicit confirmation path.

If the TUI uses a framework with weak mouse support, first look for the framework-native mouse API. If that is not enough, consider a better TUI framework before accepting reduced interaction.

## Apple-Like Visual Direction

Default visual direction: refined utility with soft polish.

- Use rounded panels, gentle spacing, and restrained color.
- Prefer quiet separators over heavy borders.
- Use one clear accent color for focus and primary action.
- Keep dense data readable, not cramped.
- Keep animation or refresh behavior smooth and non-flashing.
- Avoid flicker, full-screen churn, noisy log output, jagged box art, and overdecorated dashboards.
- Avoid ASCII clutter, excessive badges, rainbow status colors, and decorative icons that do not help navigation.
- Shorten status text. Delete command suggestions and helper copy that do not earn their pixels.

The result should feel like a focused native utility: polished, predictable, and calm.

## Design Review Checklist

Before implementing or approving a TUI change, check:

- What can the user click?
- What can the user scroll?
- What changes on hover, focus, and selection?
- Can a user complete the main task with only the mouse?
- Can a power user complete it quickly with only the keyboard?
- Does the screen remain stable during refreshes?
- Are loading, empty, error, degraded, and success states visually distinct?
- Does every visible instruction or command suggestion deserve space?
- Is the first screen immediately understandable without reading help text?
- Does the layout still work at 80x24, 120x40, and a tall narrow terminal?
- Can the state update and rendering path be debugged outside raw mode and alternate screen?
- Is there file/sidecar logging, event recording, and replay for keyboard, mouse, resize, focus, tick, and external-update events?

## Debuggable Architecture

Treat the TUI as a thin terminal shell over testable state transitions. Do not put domain behavior, persistence policy, provider calls, or business state machines directly inside key handlers or render loops.

Default structure:

```text
Terminal Event
      ->
update(state, event)
      ->
new state + commands
      ->
render(state, width, height)
      ->
frame
```

Required debugging affordances:

- Logs go to a file or structured sidecar, not stdout/stderr while the TUI owns the terminal. A human should be able to inspect logs from another shell with `tail -f app.log` or the subproject's documented equivalent.
- Keyboard, mouse, resize, focus, tick, and external-update events can be recorded in a redacted replayable format.
- Offline replay can feed recorded events through `update` and `render` without entering raw mode.
- `update(state, event)` should be deterministic where possible and return commands rather than executing wide side effects inline.
- `render(state, width, height)` should depend on explicit state and dimensions, not implicit global terminal state.
- Detail routes opened from selectable panes must carry an explicit origin snapshot. Closing the detail route must restore focus to the originating pane/list item, not the prompt, so `Up`/`Down` and `j`/`k` continue navigating the same list. Agent roster/profile detail flows are a required regression target.
- Important states and terminal sizes should have snapshot/golden tests.
- Debug mode should be able to disable alternate screen where practical, pin terminal dimensions, slow or cap refresh, and emit event/frame counters.
- Startup, normal exit, error exit, panic, and cancellation paths must restore raw mode, alternate screen, cursor visibility, and mouse capture.

## Implementation Workflow

1. Read the nearest TUI entrypoint, rendering component, keymap, and theme files.
2. Identify the framework and its mouse-event API.
3. Identify the event model, state type, command/effect boundary, and render function.
4. Add or preserve file/sidecar logging before terminal debugging.
5. Add or preserve event recording and replay before chasing interactive-only bugs.
6. Map all visible interactive regions to both keyboard and mouse behavior.
7. Preserve focus origin for every routed detail panel before adding new drill-down behavior.
8. Add or update mouse handlers before visual polish.
9. Make hover, selected, focused, disabled, and active states visually distinct.
10. Remove redundant helper text and command suggestions that compete with the main task.
11. Tune the visual system toward rounded, soft, calm Apple-like utility.
12. Verify update/render behavior with tests before relying on real terminal interaction.
13. Verify terminal integration with a manual smoke test where possible.

## Verification

Run the narrowest available checks for the TUI package, then manually smoke test:

- Replay a recorded keyboard/mouse/resize event sequence if the subproject has replay support.
- Run snapshot/golden render tests for key states and terminal sizes.
- Run debug mode with alternate screen disabled or reduced refresh when supported.
- Click tabs and nav.
- Click rows and buttons.
- Scroll lists and detail panes with the mouse wheel.
- Resize the terminal and confirm layout stability.
- Leave auto-refresh running and confirm the screen does not flash.
- Confirm keyboard shortcuts still work.
- For list-to-detail flows, verify `Enter` opens detail, `Esc` returns to the same row, and `Up`/`Down` or `j`/`k` can continue to the next row without refocusing the pane manually.
- Include a live-loop regression for any route opened from slash navigation, such as `/agent` -> `Enter` -> `Esc` -> `Down` on the Agent profile roster.
- Trigger a controlled error or cancellation path and confirm the terminal is restored.

If automated terminal mouse tests exist, run them. If not, report the manual smoke path and any behavior that could not be verified in the current environment.

## Boundaries

- Do not add mouse support to non-interactive plain CLI output.
- Do not introduce decorative motion or styling that reduces legibility.
- Do not hide essential actions behind hover-only affordances.
- Do not implement destructive mouse actions without confirmation.
- Do not accept “keyboard shortcuts are enough” for an interactive TUI unless the user explicitly waives mouse support.
- Do not debug by printing into stdout/stderr while the TUI owns the terminal.
- Do not ship a TUI whose core state changes can only be reproduced through live raw-mode interaction.
