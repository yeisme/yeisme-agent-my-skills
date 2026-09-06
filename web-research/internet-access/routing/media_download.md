# Media Download

## Purpose

Download the actual media file — video, audio, or subtitles — from a URL, as the `download` intent. This is "act on the world", not research: the deliverable is a local file, not an answer.

`yt-dlp` is the default local CLI for direct media downloads from a URL (X/Twitter, YouTube, and hundreds of other supported sites). It is not a wrapper to hide behind: run it directly, one command per task.

Probe before use:

```bash
command -v yt-dlp
yt-dlp --version
yt-dlp --list-extractors | grep -i twitter   # confirm the target extractor exists
command -v ffmpeg   # required for format merging and audio extraction
```

## Update Before Debugging

Site extractors rot continuously; X and YouTube change their internal APIs often. When an extractor fails on a URL that should work, update first, then diagnose.

```bash
yt-dlp -U                        # self-update; only works for the standalone/pip-managed binary
python -m pip install -U yt-dlp  # pip installation
brew upgrade yt-dlp              # Homebrew (wraps the PyPI wheel; -U refuses these installs)
```

`yt-dlp -U` on a package-manager install prints `You installed yt-dlp with pip or using the wheel from PyPi; Use that to update` — that is an installer hint, not a broken tool. Re-run the failed URL after updating before trying anything else.

## Probe Before Downloading

Confirm the URL resolves and see what is available before committing to a download:

```bash
yt-dlp --dump-json "URL" | jq '{title, uploader, duration, like_count}'   # metadata only, no download
yt-dlp -F "URL"                    # list formats (resolution, codec, bitrate)
yt-dlp -g "URL"                    # print direct stream URLs without downloading
yt-dlp -g -f "bv*+ba/b" "URL"      # direct URLs of the selected formats (two lines)
```

`--dump-json` doubles as the post-download verification baseline: record `duration`, `width`, `height`, and `like_count` before downloading.

## X (Twitter) Video — Worked Example

Verified 2026-09 with yt-dlp on a plain server connection, no login and no cookies. Public status videos download as a guest:

```bash
# simplest
yt-dlp "https://x.com/<user>/status/<id>"

# best quality, merged into one MP4 (recommended form)
yt-dlp -f "bv*+ba/b" --merge-output-format mp4 \
  -o "%(uploader)s/%(id)s.%(ext)s" \
  "https://x.com/<user>/status/<id>"
```

`https://twitter.com/<user>/status/<id>` URLs resolve identically.

Platform facts that shape the commands:

- X serves **video-only and audio-only HLS streams** (audio 32/64/128 kbps, video 270p to 2160p). `-f "bv*+ba/b"` selects best video + best audio and merges them; without merging you can get a silent video. `--merge-output-format mp4` keeps the container MP4 (X streams are H.264/AAC, so the merge is a remux, no re-encode).
- The **output ID can differ from the URL status ID**. X resolves a status to the tweet that physically hosts the video (observed: URL `.../status/2088796165902905540` produced file `2088796091059691520.mp4`). Never assert the URL ID as the expected filename.
- The title is usually `Uploader - Text` (the uploader name is prepended; yt-dlp issue #17617), so default filenames contain spaces and change with the tweet text. Prefer stable templates: `%(id)s.%(ext)s` or `%(uploader)s/%(id)s.%(ext)s`.
- A tweet can contain **multiple videos**; yt-dlp treats them as a playlist and downloads all entries. Use `--playlist-items 1` to pick one.
- **Login-gated content** (age-restricted, NSFW, followers-only, some media) needs a session. Prefer browser cookie import over exported cookie files:

  ```bash
  yt-dlp --cookies-from-browser chrome "URL"
  yt-dlp --cookies-from-browser firefox "URL"
  ```

- **Quoted tweets**: if the quoting status yields no video, the video lives in the quoted status — take the quoted status URL and download that directly. (Known remaining rough edge; see open yt-dlp X issues.)
- Rate limiting or `429`: add `--sleep-requests 1` and retry; if it persists, cookies usually fix it.

Never write cookies, session tokens, or auth headers into repo files, scripts, or output (see the credential rules in `agent_reach.md`).

## Generic Patterns

```bash
# cap resolution (e.g. 1080p)
yt-dlp -f "bv*[height<=1080]+ba/b[height<=1080]" --merge-output-format mp4 "URL"

# audio only
yt-dlp -x --audio-format mp3 "URL"

# subtitles without the video
yt-dlp --write-subs --write-auto-subs --sub-langs "zh-Hans,zh,en" --skip-download -o "/tmp/%(id)s" "URL"

# fixed output directory, robust retries
yt-dlp -P /tmp/downloads -o "%(uploader)s/%(id)s.%(ext)s" --retries 10 --fragment-retries 10 "URL"
```

For batch downloads keep a URL list plus a progress file and re-run to resume; `yt-dlp` skips files that already exist.

## Boundaries

- **Bilibili**: do not use yt-dlp (read or download); Bilibili risk control serves it blanket `412` responses even with cookies and proxies. Use `bili-cli` / OpenCLI per `agent_reach.md`.
- **Reading tweet text, search, or timelines** is not a download; use the Agent Reach Twitter/X backend (`twitter-cli` / OpenCLI) per `agent_reach.md`. Reading and downloading the same status often compose: read for metadata and context, yt-dlp for the file.
- Other platforms: check `yt-dlp --list-extractors`; if the site is absent or broken after an update, fall back to browser download via `browser_tools.md`.
- Do not build a dedicated download-wrapper CLI unless the user asks for reusable automation; direct commands are the contract.

## Verification

Single downloads:

```bash
ffprobe -v error -show_entries format=duration,size \
  -show_entries stream=codec_name,codec_type,width,height \
  -of default=noprint_wrappers=1 <file>
```

Check duration matches the `--dump-json` baseline, the expected streams are present (video + audio), and size is nonzero. A video-only file after an X download means the audio merge step was skipped — re-run with `-f "bv*+ba/b"`.

Batch downloads additionally follow the integrity checklist in the parent SKILL.md (count matches index, no duplicate hashes, sample first/middle/last items, no silent skips).
