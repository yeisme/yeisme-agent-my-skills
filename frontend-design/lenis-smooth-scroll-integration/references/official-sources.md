# Lenis Official Sources

Reviewed on 2026-07-18 against `lenis@1.3.25`.

- Repository and core README: https://github.com/darkroomengineering/lenis
- React integration: https://github.com/darkroomengineering/lenis/tree/main/packages/react
- Release `v1.3.25`: https://github.com/darkroomengineering/lenis/releases/tag/v1.3.25
- npm package: https://www.npmjs.com/package/lenis
- Core options: https://github.com/darkroomengineering/lenis/blob/main/packages/core/src/types.ts
- Official CSS: https://github.com/darkroomengineering/lenis/blob/main/packages/core/lenis.css

Current facts to re-check before implementation:

- The package name is `lenis`; React exports are available from `lenis/react`.
- Official CSS is imported from `lenis/dist/lenis.css`.
- React integration owns cleanup and defaults to automatic RAF unless configured otherwise.
- Core options currently have no dedicated reduced-motion switch; the application must provide the fallback.
- `allowNestedScroll` has a documented performance cost and should not be the default solution for complex applications.
- Anchor handling is opt-in.
