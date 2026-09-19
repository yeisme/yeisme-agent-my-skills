# Visual review rules

Reviewer output should be a fix list, not taste commentary.

Each issue should include:

- location or component
- observed current behavior
- expected behavior from the target or UI Spec
- likely code area to change
- severity: blocker, high, medium, low

Review dimensions:

- Layout: main/secondary hierarchy, density, alignment, scan path, key action visibility.
- Visual system: token use, semantic color count, typography scale, radius, borders, shadows, icons.
- Product: page question answered, recommended next action, empty/error/loading states, recovery path.
- Engineering: component reuse, magic numbers, responsive rules, testability, accessibility hooks.

Prefer measurable observations:

- sidebar is about 40px too narrow
- header appears 16px taller than spec
- table row height is 52px but spec says 44px
- card radius is 6px but token says 8px
- dialog animation moves 36px but spec only allows subtle 8px entry
