#!/usr/bin/env python3
"""Convert a 4x4 transparent RGBA battle sprite sheet into a looping transparent GIF.

This is a code pipeline, not an image-generation task: it reads the PNG,
splits the 16 cells (left-to-right, top-to-bottom), cleans low-alpha residue,
unifies frame sizes on transparent canvases, and encodes a transparent,
infinitely looping GIF with per-frame durations. Never redraws, rescales,
interpolates, or repaints sprite content.

Usage:
  python3 sprite_to_gif.py input.png -o output.gif
  python3 sprite_to_gif.py input.png --alpha-threshold 10 --json
"""

import argparse
import json
import sys
from pathlib import Path

from PIL import Image

COLS = ROWS = 4
FRAME_COUNT = COLS * ROWS
TRANSPARENT_INDEX = 255
PALETTE_COLORS = 255
MIN_LOOP_MS = 1500
MAX_LOOP_MS = 2000
DEFAULT_DURATIONS = [150, 140, 130, 120, 100, 70, 80, 120, 80, 90, 100, 110, 120, 130, 140, 150]


def read_sprite(path):
    im = Image.open(path)
    if im.mode != "RGBA":
        im = im.convert("RGBA")
    return im


def cell_boxes(width, height):
    xs = [round(i * width / COLS) for i in range(COLS + 1)]
    ys = [round(i * height / ROWS) for i in range(ROWS + 1)]
    return [(xs[c], ys[r], xs[c + 1], ys[r + 1]) for r in range(ROWS) for c in range(COLS)]


def split_frames(im):
    frames = [im.crop(box) for box in cell_boxes(*im.size)]
    if len(frames) != FRAME_COUNT:
        raise SystemExit(f"expected {FRAME_COUNT} cells, got {len(frames)}")
    return frames


def clean_alpha(frames, threshold):
    cleaned = []
    for f in frames:
        f = f.copy()
        if threshold > 0:
            alpha = f.getchannel("A")
            dirty = alpha.point(lambda a: 255 if a < threshold else 0)
            if dirty.getbbox():
                clear = Image.new("RGBA", f.size, (0, 0, 0, 0))
                f = Image.composite(clear, f, dirty)
        cleaned.append(f)
    return cleaned


def unify_sizes(frames):
    w = max(f.width for f in frames)
    h = max(f.height for f in frames)
    unified = []
    for f in frames:
        if f.size == (w, h):
            unified.append(f)
            continue
        canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        canvas.paste(f, (0, 0))
        unified.append(canvas)
    return unified, (w, h)


def normalize_durations(durations):
    if len(durations) != FRAME_COUNT:
        raise SystemExit(f"durations must have {FRAME_COUNT} entries")
    total = sum(durations)
    if MIN_LOOP_MS <= total <= MAX_LOOP_MS:
        return durations
    scale = (MIN_LOOP_MS + MAX_LOOP_MS) / 2 / total
    return [max(40, round(d * scale)) for d in durations]


def to_indexed(frame):
    rgb = frame.convert("RGB")
    q = rgb.quantize(colors=PALETTE_COLORS, method=Image.Quantize.MEDIANCUT)
    alpha = frame.getchannel("A")
    transparent_mask = alpha.point(lambda a: 255 if a < 128 else 0)
    q.paste(TRANSPARENT_INDEX, mask=transparent_mask)
    palette = q.getpalette()
    palette[TRANSPARENT_INDEX * 3:TRANSPARENT_INDEX * 3 + 3] = [0, 0, 0]
    q.putpalette(palette)
    return q


def encode_gif(frames, durations, out_path):
    indexed = [to_indexed(f) for f in frames]
    indexed[0].save(
        out_path,
        save_all=True,
        append_images=indexed[1:],
        duration=durations,
        loop=0,
        disposal=2,
        transparency=TRANSPARENT_INDEX,
        optimize=False,
    )


def validate(out_path, expected_size, durations):
    report = {"file": str(out_path), "checks": []}

    def check(name, ok, detail=""):
        report["checks"].append({"name": name, "ok": bool(ok), "detail": detail})
        return ok

    check("file exists", out_path.exists())
    try:
        gif = Image.open(out_path)
    except Exception as exc:  # noqa: BLE001
        check("opens", False, str(exc))
        report["ok"] = False
        return report
    check("opens", True)

    n_frames = getattr(gif, "n_frames", 1)
    check("frame count == 16", n_frames == FRAME_COUNT, str(n_frames))
    check("infinite loop", gif.info.get("loop") == 0, str(gif.info.get("loop")))

    sizes = set()
    total = 0
    first_transparency = gif.info.get("transparency")
    has_transparency = first_transparency is not None
    disposals = set()
    for i in range(n_frames):
        gif.seek(i)
        sizes.add(gif.size)
        total += gif.info.get("duration", 0)
        if gif.info.get("transparency") is not None:
            has_transparency = True
        disposals.add(getattr(gif, "disposal_method", gif.info.get("disposal", 2)))
    check("uniform frame size", len(sizes) == 1, str(sizes))
    check("size matches sprite cells", sizes == {expected_size}, f"{sizes} vs {expected_size}")
    check("loop duration in range", MIN_LOOP_MS <= total <= MAX_LOOP_MS, f"{total} ms")
    check("transparency index present", has_transparency)
    check("disposal=2 per frame", disposals <= {2}, str(disposals))
    report["size"] = list(expected_size)
    report["frames"] = n_frames
    report["total_duration_ms"] = total
    report["loop"] = gif.info.get("loop") == 0
    report["transparent"] = has_transparency
    report["ok"] = all(c["ok"] for c in report["checks"])
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="4x4 transparent RGBA PNG sprite sheet")
    parser.add_argument("-o", "--output", help="output GIF path; default <input stem>-battle.gif")
    parser.add_argument("--alpha-threshold", type=int, default=10,
                        help="alpha below this is reset to fully transparent (default 10)")
    parser.add_argument("--durations", help="16 comma-separated per-frame durations in ms")
    parser.add_argument("--json", action="store_true", help="print the validation report as JSON")
    args = parser.parse_args()

    src = Path(args.input)
    if not src.exists():
        raise SystemExit(f"input not found: {src}")
    out = Path(args.output) if args.output else src.with_name(f"{src.stem}-battle.gif")

    durations = ([int(x) for x in args.durations.split(",")] if args.durations else DEFAULT_DURATIONS)

    frames = split_frames(read_sprite(src))
    frames = clean_alpha(frames, args.alpha_threshold)
    frames, size = unify_sizes(frames)

    distinct = len({f.tobytes() for f in frames})
    if distinct < FRAME_COUNT:
        raise SystemExit(
            f"source has only {distinct} distinct frame(s) out of {FRAME_COUNT}; "
            "GIF encoding cannot preserve exact duplicate frames without altering sprite content. "
            "Fix the sprite sheet so every cell has real frame-by-frame change."
        )

    durations = normalize_durations(durations)
    encode_gif(frames, durations, out)
    report = validate(out, size, durations)

    if not report["ok"]:
        failed = [c["name"] for c in report["checks"] if not c["ok"]]
        if "loop duration in range" in failed and sum(durations) != report.get("total_duration_ms"):
            encode_gif(frames, normalize_durations(durations), out)
            report = validate(out, size, durations)
        if not report["ok"]:
            print(json.dumps(report, ensure_ascii=False, indent=2))
            raise SystemExit("validation failed after one auto-fix attempt")

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"file: {report['file']}")
        print(f"size: {report['size'][0]}x{report['size'][1]}")
        print(f"frames: {report['frames']}")
        print(f"total duration: {report['total_duration_ms']} ms")
        print(f"loop: {report['loop']}")
        print(f"transparent: {report['transparent']}")


if __name__ == "__main__":
    sys.exit(main())
