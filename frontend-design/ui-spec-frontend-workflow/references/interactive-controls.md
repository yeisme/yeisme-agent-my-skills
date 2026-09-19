## Interactive Control System

Before implementing or accepting a page, create a control inventory. Include every:

- button, icon button, segmented control, toggle, checkbox, radio, switch
- select, combobox, dropdown menu, context menu, command menu
- dialog, alert dialog, sheet/drawer, popover, hover card, tooltip
- tabs, accordion, disclosure, collapsible panel
- table filter, sort header, pagination, row action, bulk action
- image thumbnail, gallery, lightbox, preview modal, file attachment
- toast, banner, inline alert, confirmation, destructive action
- date/time picker, numeric input, search input, autocomplete

Default primitive choices for React product UIs:

| Control | Default Primitive | Required Behavior |
| --- | --- | --- |
| Simple option select | shadcn/ui or Radix Select | open/close, keyboard selection, disabled/loading/empty |
| Searchable select | Combobox with Popover + Command | typeahead, no results, async loading if remote |
| Action menu | DropdownMenu | trigger, aligned menu, keyboard navigation, disabled dangerous actions |
| Contextual detail | Popover or HoverCard | anchored positioning, outside click close, focus behavior |
| Blocking decision | AlertDialog | focus trap, Escape behavior, destructive action styling |
| Rich modal task | Dialog | title/description, focus trap, scroll body, footer actions |
| Mobile inspector | Sheet or Drawer | responsive substitution, scroll lock, close affordance |
| Image preview | Dialog/Sheet lightbox | aspect ratio, loading/error, keyboard close, optional zoom/open original |
| Feedback | Toast or inline Alert | semantic status, dismiss policy, no secret leakage |
| Data table controls | TanStack Table + design-system controls | sorting, filtering, pagination, row selection, dense data state |
| Global search | Command dialog with `cmdk` | Cmd/Ctrl+K shortcut, search, grouped results, no results, keyboard navigation |
| Charts | Recharts + semantic chart tokens | accessible labels, responsive container, stable colors, empty/error states |

Unified interaction rules:

- All overlays must use the same radius, border, shadow, background, foreground, z-index scale, and animation timing.
- All overlays must define outside click, Escape, focus trap or focus return, scroll lock, portal/container strategy, and mobile behavior.
- Icon-only controls need accessible labels and tooltip when the action is not obvious.
- Disabled controls need a reason through tooltip, inline helper, or adjacent status when the reason is not obvious.
- Loading controls must prevent duplicate destructive actions and communicate progress.
- Destructive controls require confirmation when the action is irreversible, costly, or security-sensitive.
- Image and artifact previews must avoid layout shift, preserve aspect ratio, handle load failure, and avoid exposing raw filesystem paths unless the product intentionally shows them.
- Tables must keep header, filters, row hover, selected row, empty state, and pagination visually consistent.
- Forms must use consistent label, description, error, required, disabled, dirty, saving, and saved states.
- Responsive behavior must specify whether inspectors become sheets, tables become card lists, and menus collapse into command or overflow actions.

Interaction implementation is incomplete until the main happy path and at least one failure/empty/disabled path are represented in code or tests.

