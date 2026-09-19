# GPT Image 2.5 on Eikona MCP

Live paid generate/edit prefers `openai/gpt-image-2.5-sunburst` with `quality: "high"` and pixel `size`/`aspect`. Reuse the installed GPT Image channel (`noemi` on this workspace). Do not create a channel or invent `coglet-image25`.

## Identity

- Default: `openai/gpt-image-2.5-sunburst`
- Fast draft: `openai/gpt-image-2.5-flare`
- Fallback: `openai/gpt-5.4-image-2` only if 2.5 is not ready or the user names Image 2
- Snapshots `*-2026-09-08` only when named
- Reject bare `gpt-image-2.5` (use Sunburst) and provider-colon forms
- Channel goes in `use_channels`, never in `model_ref`

## Size

Exact pixels + matching `aspect`. Never `2k`/`1k`/`4k`.

Unspecified portrait: `1152x2048` / `9:16`. Unspecified square: `2048x2048` / `1:1`. Also valid: `1024x1024`/`1:1`, `1536x1024`/`3:2`, `1024x1536`/`2:3`, `2048x1152`/`16:9`, `3840x2160`/`16:9`, `2160x3840`/`9:16`. 4K is 3840 long-edge, not `4096x4096`.

## Coglet overlay (historical only)

`coglet-image25` + `execution_mode=foreground` + `quality=medium` was a 2026-09-11 verification, not this workspace default. Missing that channel is expected. Use `use_channels: ["noemi"]` (or whatever `auth list` / MCP discovery shows).
