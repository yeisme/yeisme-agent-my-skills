# Agent Reach Route

## Purpose

Use Agent Reach when an internet task targets platforms where ordinary static search or scraping is fragile: Twitter/X, Reddit, YouTube, Bilibili, XiaoHongShu, LinkedIn, V2EX, Xueqiu, Xiaoyuzhou podcasts, RSS, or general multi-platform web access setup.

Agent Reach is a capability layer: it installs, selects, health-checks, and explains platform backends. It is not the content wrapper. After `agent-reach doctor` identifies the active route, call the selected upstream tool directly.

## When To Use

Use this route when:

- The user asks to install, update, configure, or diagnose Agent Reach.
- The task mentions a supported platform such as Twitter/X, Reddit, YouTube, Bilibili, XiaoHongShu, LinkedIn, V2EX, Xueqiu, Xiaoyuzhou, or RSS.
- A platform needs login cookies, browser session reuse, a proxy, or multiple fallback backends.
- Static `firecrawl scrape`, `curl`, or direct page reading is insufficient.

Do not use this route when:

- The task is a normal public documentation lookup or source discovery. Use `firecrawl`, `gh`, package-manager CLIs, or `curl` first.
- The user needs visible page operation, form submission, screenshots, or dynamic UI state. Use `browser_tools.md` after this route if Agent Reach cannot provide a readable backend.
- The task belongs to Yeisme/Hermes/OpenWebUI local research infrastructure. Use `local_research_infra.md` first.

## Install And Diagnose

Check whether the CLI exists:

```bash
command -v agent-reach
agent-reach --version
```

If missing, prefer a user-level install. Keep files outside the current project workspace:

```bash
pipx install https://github.com/Panniantong/agent-reach/archive/main.zip
agent-reach install --env=auto
```

If `pipx` is unavailable or Python packaging policy blocks direct install, use a user-level virtual environment:

```bash
python3 -m venv ~/.agent-reach-venv
source ~/.agent-reach-venv/bin/activate
pip install https://github.com/Panniantong/agent-reach/archive/main.zip
agent-reach install --env=auto
```

For a preview or security-conscious machine:

```bash
agent-reach install --env=auto --safe
agent-reach install --env=auto --dry-run
```

Diagnose before selecting tools:

```bash
agent-reach doctor
agent-reach doctor --json
```

Use the doctor result to report:

- ready channels.
- unavailable channels.
- active backend for the requested platform.
- missing credentials, browser extension, proxy, or optional package.

## Optional Channels

Only install optional channels that the user needs:

```bash
agent-reach install --env=auto --channels=opencli,twitter,reddit,bilibili
agent-reach install --env=auto --channels=xiaohongshu
agent-reach install --env=auto --channels=all
```

Supported channel names include `opencli`, `twitter`, `xiaoyuzhou`, `xueqiu`, `xiaohongshu`, `reddit`, `bilibili`, `linkedin`, and `all`.

Ask before installing `all` because it may install more tools than the immediate task needs.

## Platform Routing

After `agent-reach doctor`, prefer the reported backend. Common examples:

| Platform | Common backend | Use pattern |
| --- | --- | --- |
| Web page | Jina Reader / `curl` | Read clean content from a URL. |
| GitHub | `gh` | Use structured repo, issue, release, PR commands. |
| YouTube | `yt-dlp` | Extract metadata, subtitles, or video search output. |
| Bilibili | `bili-cli` / OpenCLI | Search and video detail; use OpenCLI for logged-in or subtitle cases when configured. |
| Twitter/X | `twitter-cli` / OpenCLI | Read tweets; cookies unlock search, timeline, and long-form content. |
| Reddit | OpenCLI / `rdt-cli` | Requires login state; anonymous route is unreliable. |
| XiaoHongShu | OpenCLI / xiaohongshu-mcp / xhs-cli | Desktop prefers browser session; server may need MCP QR login. |
| RSS | `feedparser` | Parse feeds directly. |
| Xiaoyuzhou | transcription backend | Transcribe podcast audio after key configuration. |

Do not assume these commands are installed solely because Agent Reach exists. Confirm through `agent-reach doctor` or direct `command -v <tool>` before use.

## Credentials And Proxy

Real credentials must stay in user-level local config or secret stores. Never write cookies, tokens, API keys, Authorization headers, or raw provider payloads into repo files, docs, run evidence, screenshots, or final answers.

Browser cookie import:

```bash
agent-reach configure --from-browser chrome
```

Manual cookie import, only when the user explicitly provides the cookie string:

```bash
agent-reach configure twitter-cookies "PASTED_COOKIE_HEADER"
agent-reach configure xhs-cookies "PASTED_COOKIE_HEADER"
```

Proxy for restricted networks:

```bash
agent-reach configure proxy http://user:pass@ip:port
```

If a task needs login, cookie export, QR scan, paid action, account modification, posting, or destructive form submission, pause for explicit user confirmation.

## Safety Boundaries

- Do not run `sudo` unless the user explicitly approves it.
- Do not clone upstream tools or write generated files inside the user's project workspace.
- Do not add shell credential scripts as a persistence layer.
- Do not expose cookie strings, proxy passwords, tokens, local browser profile paths, or secret config values.
- Use dedicated or secondary accounts for risky cookie-based platforms when advising the user.
- Respect rate limits, platform terms, and authentication boundaries.

## Output Format

```markdown
**Route**: Agent Reach
**Doctor**: [ready / partial / missing]
**Platform**: [target platform]
**Active backend**: [backend reported or checked]
**Completed**: [what was read, searched, extracted, or configured]
**Blocked**: [credentials, login, proxy, install permission, or unavailable backend]
**Evidence**: [URLs, command category, screenshots/artifacts if any]
```

For simple successful tasks, a shorter answer is fine. Always mention when content coverage depends on authenticated state or a fallback backend.
