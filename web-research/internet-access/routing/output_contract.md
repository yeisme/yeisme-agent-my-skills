# Output Contract

## Purpose

Make internet information access answers stable, auditable, and not overly long.

## General Requirements

Every internet-dependent answer should include:

- conclusion or result.
- source URL or source name.
- key limitations or uncertainty.
- freshness notes for high-change information.

## `lookup` Output

```markdown
**Answer**: [direct answer]

**Source**: [URL or structured source]
```

For version/status:

```markdown
**Answer**: [current version/status]
**Updated**: [source update time, if available]
**Source**: [URL]
```

## `research` Output

```markdown
**Summary**
[3-5 sentences]

**Findings**
- [finding] (source)
- [finding] (source)

**Limits**
- [information gap, staleness risk, or conflict]

**Sources**
- [title/domain] - [URL]
```

## `local-research-infra` Output

```markdown
**Route Decision**
- Context: [host CLI / OpenWebUI internal / Hermes Research Harness / Gateway policy]
- Recommended route: [firecrawl CLI / SearXNG + Firecrawl loader / Research Harness / browser escalation]

**Local Configuration Evidence**
- Firecrawl: [URL/config source]
- SearXNG: [URL/config source]
- Research Harness: [profile, trace, or valve]
- Disabled backend: [for example, BigModel/Zai web-search-prime]

**Verified**
- [commands or checks, without secrets]

**Next Step**
- [continue search, expand budget, inspect trace, adjust query, escalate browser, or run health check]
```

## `deep-research` Output

```markdown
**Research Question**
[question and boundaries]

**Method**
- Query batches: [count]
- Candidate sources: [count]
- Deduped sources: [count]
- Included samples: [count]
- Exclusion rules: [rules]

**Category Statistics**
| Category | Count | Representative samples |
| --- | ---: | --- |
| [category] | [n] | [source] |

**Key Findings**
- [finding] (evidence/sample)

**Evidence Matrix**
| Sample | Category | Key fields | Source |
| --- | --- | --- | --- |
| [name] | [category] | [fields] | [URL] |

**Limits**
- [coverage, search bias, access limits, time range]
```

If the user asks for 200/300 examples, the final answer may show category statistics and representative samples, but it must say where the full sample table is stored or continue in batches.

If the full sample is too large:

- If the user explicitly asks for a file, save it to the user-specified path.
- If no path is specified, do not create a file by default; show category statistics and representative samples, then say the full ledger can be continued.
- If a file was created, state the path, record count, and fields.

## `verify` Output

```markdown
**Conclusion**: [true / false / partially true / insufficient evidence]

**Basis**
- [supporting evidence] (source)
- [contrary or conflicting evidence] (source)

**Confidence**: [high / medium / low]
**Notes**: [freshness, scope, or definition issue]
```

## `extract` Output

```markdown
**Extracted Results**
| Field | Value | Source |
| --- | --- | --- |
| [field] | [value] | [URL/API/CLI] |

**Missing Fields**
- [field that could not be obtained and why]
```

## `interact` Output

```markdown
**Execution Summary**
- Tool: [agent-browser / browser-use / Playwright]
- Final URL: [URL]
- Completed: [successful operations]
- Blocked: [permission, login, CAPTCHA, paywall, or other limits]

**Evidence**
- Screenshot: [path]
- Download: [path]
- Other: [console/errors/network, if any]
```

## `automate` Output

```markdown
**Automation Recommendation**
- Recommended method: [existing project command / npx playwright / agent-browser exploration then hardening]
- Reason: [why repeatable automation is needed]
- Risks: [login state, selectors, rate limits, terms]
- Verification command: [real command]
```

## Failure Or Blocked Output

```markdown
**Result**: Could not complete.

**Reason**: [missing tool / insufficient permissions / login required / page blocked / source unavailable]

**Tried**
- [command or tool]

**Next Step**
- [what is needed from the user or recommended fallback]
```
