# Evidence Policy

## Purpose

Prevent agents from treating search summaries, second-hand articles, or old pages as final facts. Every internet-dependent claim should have a clear evidence level.

## Evidence Levels

| Level | Evidence type | Use for |
| --- | --- | --- |
| L1 | Search result summaries, snippets | Leads and candidate sources, not final key evidence |
| L2 | Regular web page text, blogs, press releases | General background and low-risk facts |
| L3 | Official docs, release notes, standards, papers, source repositories | Technical conclusions, product/API behavior, version notes |
| L4 | Structured CLI/API output, such as `gh`, `npm view`, `curl` + `jq` | Current status, versions, update time, repository metadata |
| L5 | Real browser page state, screenshots, downloaded files, console/network evidence | UI state, logged-in state, dynamic content, interaction results |

## Usage Rules

- `lookup` needs at least L2; versions, releases, and repository metadata should prefer L4.
- `research` needs multiple L2/L3 sources; technical guidance should prefer L3.
- `deep-research` must distinguish candidate sources, included samples, and final citations; final conclusions need an evidence matrix or category statistics.
- `verify` must prefer L3/L4; list conflicting sources when disputed.
- `extract` should prefer L4 or direct URL extraction.
- `interact` needs L5, with at least final URL or screenshot path recorded.

## Source Credibility

Priority:

1. Official docs, standards, papers, source repositories, release notes.
2. Official API or CLI output.
3. Issues, discussions, or blogs from project maintainers.
4. Third-party tutorials, media reports, community discussion.
5. Search summaries.

## Citation Requirements

Final answers should:

- Provide URLs or clear source names.
- State evidence level or confidence for high-impact claims.
- Say "insufficient evidence" when uncertain.
- Avoid merging conflicting sources into a single overconfident conclusion.

## Unacceptable Evidence

- Answering current information from model memory only.
- Using only search snippets for key conclusions.
- Guessing GitHub/npm/PyPI/Cargo/Go metadata from screenshots or web pages when structured sources exist.
- Concluding logged-in or dynamic state without browser evidence.
- Claiming "the whole web", "comprehensive", or "200 cases" without candidate counts, dedupe rules, inclusion criteria, and sample statistics.
