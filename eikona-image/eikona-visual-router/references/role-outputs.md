# Visual Operator Role Outputs

Shared reference for Eikona Visual Operators. One level deep from SKILL.md.

## Role templates

Each role has a required contribution shape. Directors emit their fields into a `visual_intent.v1` envelope; they do not execute providers or mutate run state.

### Router

- Selects scenario, skill roles, and rationale
- Emits `skill_chain` with at most 1 router + 1 domain_router + 1 readiness_gate + 1 primary_director
- Identifies unresolved inputs

### Readiness gate

- Emits monotonic `readiness.status`, `blocking_codes`, `evidence_refs`, `allowed_mode`
- Cannot be weakened by lower-authority sources
- `candidate_only` or `blocked` restricts production compilation

### Primary director

- Emits creative constraints: `canvas`, `content_constraints`, `references`, `reference_mode`, `review_rubric`
- Does not choose models, widen permissions, or access credentials
- Returns declarative intent fields and evidence references only

### Runtime

- Validates and compiles intent into existing workflow DAG
- Writes `visual_intent.json`, `skill_receipt.json`, `intent_compile.json`
- Owns run evidence, review, feedback, handoff
- Model/provider/credential resolution is runtime responsibility

## Composition rules

```
one public router
  → zero or one domain context router
  → zero or one readiness gate
  → exactly one primary director
  → Eikona intent compiler/runtime
```

Child skills refine the envelope but may not: choose models/agents, widen permissions, spawn descendants, execute providers, or mutate run state.

## Boundary: Prompt Modules vs Visual Operators

- **Visual Operator** = executable Agent Skill (this contract)
- **Prompt Module** = render-only prompt skill asset (`eikona prompts skill ...`)
- Prompt Modules cannot invoke Visual Operators or execute shell/provider commands
- Visual Operators reference Prompt Modules by identity (`eikona://prompt/<id>`)
