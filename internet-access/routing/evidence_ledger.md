# Evidence Ledger

## Purpose

Provide traceable records for deep research and large-sample arguments. Agents must distinguish candidate sources, deduplicated sources, included samples, excluded samples, and final citations.

## Ledger Levels

| Level | Meaning |
| --- | --- |
| candidate | Raw candidate found by search, CLI, API, or browser |
| deduped | Candidate after deduplication |
| included | Sample that matches inclusion criteria |
| excluded | Candidate excluded with a reason |
| cited | Representative source cited in the final answer |

## Recommended Fields

| Field | Description |
| --- | --- |
| id | Stable identifier |
| name | Project, product, company, or source name |
| canonical_url | Canonical URL |
| source_type | docs / GitHub / registry / API / paper / blog / news / browser |
| discovery_query | Query or command that found it |
| tool | firecrawl / gh / npm / curl / agent-browser |
| raw_url | Original URL |
| dedupe_key | URL, owner/repo, package name, or domain |
| included | yes/no |
| exclusion_reason | Reason for exclusion |
| category | Classification |
| fields | Extracted key fields |
| evidence_level | L1-L5 |
| last_updated | Source update time |
| confidence | high / medium / low |
| notes | Notes |

## Markdown Ledger Format

Small samples can be shown directly in the answer:

```markdown
| id | name | category | evidence | source |
| --- | --- | --- | --- | --- |
| S001 | Example | open-source | L4 | https://example.com |
```

## JSONL Ledger Format

Large samples are better as JSONL. Create a file only when the user asks to save the full list or when the sample is too large to display:

```jsonl
{"id":"S001","name":"Example","canonical_url":"https://example.com","source_type":"docs","included":true,"category":"platform","evidence_level":"L3"}
```

If a file is created, use the user-specified path. If no path is specified, explain the suggested path and get consent, unless the task explicitly asks for a file deliverable.

## Deduplication Rules

Dedupe key priority:

1. GitHub `owner/repo`.
2. package name.
3. canonical URL.
4. domain + product name.
5. title + organization.

## Exclusion Reasons

Common exclusion reasons:

- duplicate.
- irrelevant.
- inaccessible.
- low_quality_aggregator.
- no_primary_source.
- outside_scope.
- stale_or_inactive.
- insufficient_evidence.

## Summary Metrics

Deep research output must report at least:

- candidates_total
- deduped_total
- included_total
- excluded_total
- cited_total
- batches_total
- duplicate_rate
- inclusion_rate

## Quality Requirements

- Every key finding should trace back to a ledger source.
- Final citations should represent distinct categories and evidence levels; more citations are not automatically better.
- If the full ledger is not output, state whether the displayed table is representative or complete.
