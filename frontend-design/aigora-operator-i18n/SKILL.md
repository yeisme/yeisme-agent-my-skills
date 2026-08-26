---
name: aigora-operator-i18n
description: Use when adding, changing, testing, or reviewing user-visible copy, locale behavior, accessibility labels, tables, forms, filters, commands, status text, or responsive layout in the Aigora Operator Console, where zh-CN/en-US parity and protocol-safe translation boundaries must be preserved.
---

# Aigora Operator i18n

Apply the Aigora Operator Console's single `I18nProvider` contract. The product specification is `apigateway/aigora/docs/operator-console-i18n-ui-spec.md`; this skill turns it into an execution and verification workflow.

## Invariants

- `zh-CN` is the default locale and `en-US` is the required reviewed adaptation.
- Translation changes user-visible labels only. API/CLI/JSON fields, routes, operation IDs, provider/model names, capability IDs, reason codes, resource IDs, paths, scopes, status facts, and audit fields remain stable original values.
- Locale changes update React copy and `<html lang>` without reloading the page or clearing scope, Context Deck state, filters, forms, or drafts.
- Use the shared `I18nProvider` and `useI18n().t()` path. Do not add page-local locale stores, parallel dictionaries, or inline `locale === ...` branches.
- Missing keys fall back visibly from selected locale to `zh-CN`, then to a stable fallback/raw key. Never hide missing copy with an empty string.
- Authorization, redaction, copy safety, selectors, and audit logic must use raw keys/IDs, not translated labels.

## Workflow

1. Inventory rendered headings, descriptions, columns, filters, fields, validation, empty/loading/error states, confirmations, tooltips, live regions, and accessible labels for the affected surface.
2. Reuse an existing namespace in `web/operator/src/i18n/index.tsx`; add both `zh-CN` and `en-US` entries and use variables for IDs, counts, and titles.
3. Keep dynamic schemas, column definitions, and status maps locale-aware. Do not freeze translated text in module-level constants that cannot react to locale changes.
4. Cover shared defaults, mobile `Sheet`/`Dialog` close controls, `EvidenceRail`, `CommandGuard`, Context Deck, and live regions when the changed flow uses them.
5. Use stable IDs, `data-slot`, or test IDs for interaction logic. Do not make DOM behavior depend on one locale's aria text.
6. Verify `en-US` page title, navigation, key actions, and at least one loading/empty/error state. Confirm language switching preserves scope, filters, open context, focus, and drafts.
7. Review longer English copy for overflow, `min-w-0`, truncation/wrapping, mobile layout, tooltip access, and keyboard operation.

## Validation

From `apigateway/aigora/web/operator` run the narrowest relevant tests, then:

```bash
bun run check:i18n
bunx tsc --noEmit
bun run test
bun run build
```

For the critical language-switch path:

```bash
bun run test:e2e -- e2e/i18n-page-polish-e2e.spec.ts
```

Report the dictionary/page scope, focused tests, build result, preview locale, `<html lang>`, preserved state, untranslated protocol-owned values, and any pre-existing `bun run check` blockers.
