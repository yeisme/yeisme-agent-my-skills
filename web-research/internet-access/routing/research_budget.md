# Research Budget And Stopping Conditions

## Purpose

Control effort, sample size, and stopping points for deep research. Avoid endless search, and avoid presenting a few sources as large-sample research.

## Budget Dimensions

Before execution, confirm or set:

- target candidate count.
- target included sample count.
- query batch count.
- results per batch.
- source type coverage.
- time range.
- whether a full ledger is required.
- whether file creation is allowed.

## Default Budgets

| Task | Query batches | Candidate sources | Included samples | Output |
| --- | ---: | ---: | ---: | --- |
| quick scan | 3-5 | 20-50 | 10-20 | Summary + representative samples |
| standard scan | 5-10 | 50-120 | 20-50 | Category stats + evidence table |
| large scan | 10-20 | 120-300 | 50-150 | Category stats + representative samples + ledger |
| exhaustive attempt | 20+ | 300+ | 100+ | Requires explicit scope and delivery format |

## Stopping Conditions

Stop when any of these is true:

- The user-specified sample target is reached.
- Two consecutive query batches add fewer than 20% new valid samples.
- Each key category has at least 3 representative samples.
- Major primary sources are covered.
- Further search adds mostly duplicates or low-quality sources.
- Time, tools, or access permissions reach the limit.

## Escalation Conditions

Escalate from standard to deep-research when:

- The user asks for 50+ real cases.
- The user asks for "the whole web", "systematic", or "as comprehensive as possible".
- The conclusion needs category statistics or coverage.
- Initial search shows a complex ecosystem and 5-10 sources are insufficient.

Escalate from deep-research to browser when:

- Static sources cannot confirm key samples.
- Screenshots or real page state are needed.
- Logged-in data is required.

Escalate from Hermes/OpenWebUI Research Harness to CLI deep-research when:

- The user asks for 100/200/300 examples, beyond current OpenWebUI valves or one-run trace budget.
- A full candidate ledger, dedupe table, classification matrix, or cross-batch statistics are required.
- Research Harness trace shows `search_scarcity`, `domain_scarcity`, or budget clamp.
- The task needs mixed `firecrawl`, `gh`, package manager, registry, and API data.

After escalation, you may reuse Research Harness query buckets and trace as the first evidence batch, but manage the full research through `deep_research.md` and `evidence_ledger.md`.

## Degradation Conditions

Degrade from deep-research to standard when:

- The user really needs only directional judgment.
- The requested sample size has no clear value.
- Tools are unavailable and samples cannot be collected reliably.
- Time is insufficient for large-sample dedupe and extraction.

When degrading, state:

```markdown
This task can first use a standard scan for a directional conclusion. A 200+ sample result requires additional batches, deduplication, and an evidence ledger.
```

## Reporting Incomplete Large-Sample Work

If the user asks for 200/300 examples but the current run cannot complete it reliably, output:

- query batches executed.
- candidates discovered.
- deduped count.
- included sample count.
- current category coverage.
- main gaps.
- next query plan.
- if Research Harness was involved, trace path, coverage limits, budget clamp, and whether host CLI batch continuation is needed.

Do not package incomplete work as a complete study.
