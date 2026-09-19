# React animation and dependency policy

Do not install an animation library by default. First inspect the owning app's `package.json` and existing tokens/components, then use the current CSS, Web Animations, Radix `data-state`, or approved project motion capability. Run `yeisme-ui-motion-quality` after implementation for a focused motion review.

Use this selection rule:

| Scenario | Default choice |
| --- | --- |
| Page transitions, cards, tabs, drawers, modal panels, hover/tap micro-interactions | Existing project capability; CSS/Radix first for simple state changes |
| List, table row, task card, grid item add/remove/filter/reorder | CSS/Web Animations or an existing layout-transition capability; do not add AutoAnimate only for convenience |
| shadcn/ui or Radix Dialog, Popover, Dropdown, Tooltip, Accordion, Tabs | Radix `data-state` plus Tailwind/CSS animation |
| Complex marketing scroll animation, SVG timeline, hero animation | GSAP only when explicitly required and approved by the owning project |
| Physics, elastic gestures, 3D or react-three-fiber motion | React Spring only when explicitly required and already compatible |
| Empty-state illustration, loading illustration, success/failure animation asset | Lottie only when an actual animation asset exists |
| Legacy CSS enter/exit lifecycle | React Transition Group only for existing projects already using it |

Animation rules:

- Keep ordinary UI transitions short, calm, interruptible, and subordinate to the UI Spec; a 120ms–240ms range is a starting point, not a contract.
- Use `ease-out` for standard UI motion and `cubic-bezier(0.16, 1, 0.3, 1)` for emphasized but still calm transitions.
- Do not use large movement, strong bounce, rotation, particles, glow effects, or decorative animation in dashboards, admin screens, engineering tools, or terminal-like web UIs.
- Do not change layout structure to create animation, and do not gate content visibility on a reveal class.
- Animation should explain state change: enter, exit, expand, collapse, reorder, select, hover, loading, success, or failure.
- Always support `prefers-reduced-motion`; remove nonessential transforms while preserving state, focus, error, and content changes.
- Verify animation does not create layout shift, text overlap, scroll jumps, focus loss, or screenshot instability.

React dependency rules:

- Inspect the owning app's `package.json` before adding dependencies.
- Do not install duplicate animation libraries that overlap with an existing project standard.
- Prefer `motion` over older Framer Motion package usage for new React code when the project has no existing standard.
- Prefer CSS/Radix `data-state` animation for primitive open/close behavior over wrapping every primitive in Motion.
- Add GSAP, React Spring, Lottie, or React Transition Group only when the UI Spec names the scenario and the existing project does not already solve it.
