# GPT Image 2.5 (Sunburst / Flare)

Owner docs: `cli/eikona/docs/commands/models.md`, `cli/eikona/docs/product/precision-edit-image25.md`, `cli/eikona/docs/commands/image25-mcp.md`.

## Live preference (this workspace)

Paid Eikona generate/edit on the existing GPT Image gateway uses the 2.5 series. Reuse the already configured channel and key (`noemi` on this machine; otherwise the current `eikona auth list` GPT Image channel). Do **not** create a new channel, ask for a new key, or invent `coglet-image25`.

| Priority | Ref | When |
| --- | --- | --- |
| Default live | `openai/gpt-image-2.5-sunburst` | Unspecified paid generate/edit; user asked for high quality |
| Fast / cheap | `openai/gpt-image-2.5-flare` | User asked for speed, draft, or Flare |
| Snapshot | `*-2026-09-08` | User named that snapshot |
| Fallback | `openai/gpt-5.4-image-2` | 2.5 not ready on this channel, or user named Image 2 |
| Preview | `codex:imagegen` | No paid gateway; 1K Codex session only |

Default 2.5 quality is `high`. Use `xhigh`/`max` only when the user asks for maximum quality. `medium` is a historical coglet verification overlay, not this gateway's preference.

`openai/gpt-5.4-image-2` remains a gateway identity, not official `gpt-image-2`. Builtin CLI default may still list it; agent commands must still pass the 2.5 slash ref until a user/channel default is set.

## Identity rules

- Reject bare `gpt-image-2.5`. If the user says only “2.5”, use Sunburst.
- Reject `openai:gpt-image-2.5-sunburst` / duplicated provider prefixes before submit.
- Channel names are config, never part of `model_ref`.
- Do not put a GPT Image ref in a Responses top-level/analysis model.

## Size vocabulary

Image 2.5 is pixel-capable. Do **not** send `--size 2k|1k|4k`.

| Class | size | aspect |
| --- | --- | --- |
| 1K square | `1024x1024` | `1:1` |
| 1K landscape | `1536x1024` | `3:2` |
| 1K portrait | `1024x1536` | `2:3` |
| 2K square | `2048x2048` | `1:1` |
| 2K landscape | `2048x1152` | `16:9` |
| 2K portrait | `1152x2048` | `9:16` |
| 4K landscape | `3840x2160` | `16:9` |
| 4K portrait | `2160x3840` | `9:16` |

Unspecified portrait live generate: `1152x2048` + `9:16`. Unspecified square: `2048x2048` + `1:1`. 4K is 3840 long-edge, not `4096x4096`. Always send matching `--size WxH` and `--aspect W:H`.

## CLI examples

```bash
eikona auth list --agent
eikona generate --use-channel noemi --model openai/gpt-image-2.5-sunburst --size 1152x2048 --aspect 9:16 --quality high --prompt "user image intent" --dry-run --agent
eikona generate --use-channel noemi --model openai/gpt-image-2.5-sunburst --size 1152x2048 --aspect 9:16 --quality high --prompt "user image intent" --agent
```

Replace `noemi` only when `auth list` shows a different GPT Image channel. Edit stays on `eikona edit` / precision-edit; prefer Sunburst for precision edit.

## MCP overlay

Same model/size/quality preference. `use_channels` must be the installed GPT Image channel (here: `noemi`). The 2026-09-11 `coglet-image25` + `quality=medium` + `execution_mode=foreground` card is historical verification, not this workspace default. Read `eikona://docs/image25-mcp` only when that resource matches the installed server.
