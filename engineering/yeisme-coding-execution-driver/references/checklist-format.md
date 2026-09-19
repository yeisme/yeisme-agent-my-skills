## Live Checklist Format

Use the plan/update tool when available. If writing the checklist in text, use this compact format:

```markdown
- [ ] P0 Goal: Implement <outcome>
- [ ] P0 Phase: <capability> (depends: none)
- [ ] P0 Task: <slice> (depends: probe-api, verify: npm test path)
- [ ] P0 Step: <leaf action> (depends: none, verify: command)
- [~] P0 Step: <active leaf>
- [x] P1 Step: <verified leaf> (evidence: command passed)
- [!] P0 Step: <blocked leaf> (needs: credential/user decision)
- [-] P3 Step: <cut leaf> (reason: out of scope)
```

Legend:

- `[ ]` pending
- `[~]` in progress
- `[x]` done
- `[!]` blocked
- `[-]` cut

