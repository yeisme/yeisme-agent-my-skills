---
name: anatomia-scaena-learning-loop
description: Use when turning reviewed Anatomia analyses, dataset decisions, prompt evaluations, Scaena production reviews, quality findings, asset reuse, or real outcomes into scoped learning candidates, recipe or blueprint influence, viral patterns, evaluation evidence, or OpenSpec-ready capability proposals for Anatomia and Scaena Studio.
---

# Anatomia Scaena Learning Loop

Build verified product learning. Do not treat model output, one correction, synthetic fixtures, page existence, or a successful tool call as proof that the system learned.

## Inputs

- Anatomia analysis/revision/evaluation refs.
- Scaena review, ProductionGraph, quality, prompt, dataset, asset, OutcomeRecord or CreatorRecipePack refs.
- Evidence eligibility, scope, baseline and target owner.

## Workflow

1. Classify evidence as synthetic, human-attested real, imported real, legacy, or ineligible.
2. Determine learning scope: project, creator, domain, model, platform, organization, or public-safe abstraction.
3. Create a candidate from review diff, evaluation, quality finding, dataset decision, outcome or repeated blocker.
4. Run a held-out or compatible second-run evaluation with baseline, cost, limitations and redacted evidence.
5. Record `improved`, `regressed`, `no_observed_change`, or `inconclusive` honestly.
6. Route validated creator production learning to Scaena recipe/blueprint/pattern review.
7. Route repeated capability gaps to the owning OpenSpec as a proposal; never modify production code as a learning action.

## Planned Commands

```bash
anatomia learning candidate list --status candidate --json
anatomia learning evaluate <candidate-ref> --suite heldout-v1 --json
anatomia learning review <candidate-ref> --decision accept --json
anatomia capability propose --from-gap <gap-ref> --target scaena --json
anatomia learning handoff scaena <candidate-ref> --json
scaena outcome import --from ./metrics.csv --package <package-ref> --json
scaena pack promote --from-outcome <outcome-ref> --json
```

These commands are planned contracts until their owning OpenSpec tasks are implemented and verified. Do not claim they currently execute.

## Promotion Gates

- One correction creates only a candidate or eval case.
- Synthetic evidence proves engineering flow only.
- Active recipe, Prompt Blueprint, director rule or viral pattern requires evaluation and human/owner decision.
- Private creator/project learning does not silently become public or cross-tenant knowledge.
- Permission revocation invalidates dependent dataset, asset, recipe and pattern eligibility.
- Second-run influence must identify changed fields and source refs.

## Capability Proposals

A proposal must include target owner, repeated evidence, affected users, contract surfaces, acceptance metrics, test/evidence plan, risk, rollback and suggested OpenSpec path. `accepted` does not mean `delivered`.

## Boundaries

- Never fabricate platform metrics, user adoption, quality improvement or paid signal.
- Never store credentials, raw prompts, provider payloads, private tool arguments, hidden prompts or full reasoning.
- Never let an Agent approve its own high-risk output or mutate tracked source through the learning workflow.
- Anatomia owns observation/evaluation candidates; Scaena owns production decisions, outcomes and creator recipes.

## Output

Return evidence class, scope, candidate/evaluation/influence/proposal refs, result, limitations, owner, review state, next real command and whether implementation is still pending.

## Validation

```bash
anatomia learning show <candidate-ref> --json
scaena outcome show <outcome-ref> --json
openspec validate --all --strict
```
