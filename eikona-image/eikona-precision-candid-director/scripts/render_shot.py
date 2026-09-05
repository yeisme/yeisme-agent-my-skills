#!/usr/bin/env python3
"""Render a precision-parameterized candid shot prompt from a shot spec.

Each shot spec (assets/shots/<id>.json) fully determines one image: subject,
pose, camera height/lens/framing, foreground coverage, two-source lighting,
quantified palette ratios, scene fingerprints, quality tail, negatives. The
renderer assembles the English prompt in a fixed slot order, writes the prompt
file, manifest.json (namespaced tags) and runbook.yaml following the
eikona-file-prompt-workflow prompt library convention.

Examples:
  python3 render_shot.py --shot night-bedroom-lookback \
      --out prompts/generic/precision-candid/night-bedroom-lookback
  python3 render_shot.py --list-shots
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
SHOTS_DIR = SKILL_ROOT / "assets" / "shots"


def load_shot(shot_id):
    path = SHOTS_DIR / f"{shot_id}.json"
    if not path.exists():
        raise SystemExit(f"unknown shot: {shot_id} (looked for {path})")
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def combo_id(spec, aspect):
    raw = json.dumps(spec, ensure_ascii=False, sort_keys=True) + f"|{aspect}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:8]


def compute_tags(spec, aspect):
    tags = [
        "style:precision-candid",
        f"shot:{spec['id']}",
        f"aspect:{aspect}",
        f"subject:{spec['subject']['id']}",
        f"lens:{slug(spec['camera']['lens'])}",
        f"light.temperature:{spec['light']['temperature']}",
    ]
    if spec.get("palette"):
        tags.append(f"palette.primary:{slug(spec['palette'][0]['color'])}")
    tags += [f"fingerprint:{slug(f)}" for f in spec.get("fingerprints", [])]
    tags += [f"use:{u}" for u in spec["tags"]["use"]]
    tags += [f"mood:{m}" for m in spec["tags"]["mood"]]
    return tags


SOLUTION_ID = "precision-candid-shot"


def find_repository():
    for base in [Path.cwd(), *Path.cwd().parents]:
        if (base / "data" / "yeisme-prompt-templates" / "repository.json").exists():
            return base / "data" / "yeisme-prompt-templates"
    raise SystemExit(
        "template repository not found; run from the yeisme-agent workspace or pass --template"
    )


def load_template(locale, override=None):
    path = Path(override) if override else (
        find_repository() / "solutions" / "image" / SOLUTION_ID / "prompts" / f"main.{locale}.md"
    )
    if not path.exists():
        raise SystemExit(f"template not found: {path}")
    return path.read_text(encoding="utf-8")


def build_bindings(spec, aspect):
    s, c, l = spec["subject"], spec["camera"], spec["light"]
    if c.get("position"):
        position = f"Camera positioned {c['position']}"
    else:
        position = f"Camera height {c['height']}"
    f = spec.get("foreground")
    return {
        "orientation": spec["orientation"],
        "aspect": aspect,
        "subject_description": s["description"],
        "pose": s["pose"],
        "expression": s["expression"],
        "pronoun": s["pronoun"],
        "wardrobe": s["wardrobe"],
        "camera_position_clause": position,
        "lens": c["lens"],
        "perspective_clause": f", {c['perspective']}" if c.get("perspective") else "",
        "framing": c["framing"],
        "foreground_sentence": f" {f['elements']} cover {f['coverage']}." if f else "",
        "light_key": l["key"],
        "light_fill_clause": f", {l['fill']}" if l.get("fill") else "",
        "palette_sentence": (
            " Main colors: "
            + ", ".join(f"{p['pct']}% {p['color']}" for p in spec["palette"]) + "."
            if spec.get("palette") else ""
        ),
        "background_sentence": (
            " " + spec["background"][0].upper() + spec["background"][1:] + "."
            if spec.get("background") else ""
        ),
        "fingerprints_sentence": (
            f" Scene fingerprints: {', '.join(spec['fingerprints'])}."
            if spec.get("fingerprints") else ""
        ),
        "quality": ", ".join(spec["quality"]),
        "atmosphere": spec["atmosphere"],
        "negatives": ", ".join(f"no {n}" for n in spec["negative"]),
        "tail_clause": ", " + ", ".join(spec["tail"]) if spec.get("tail") else "",
    }


def render_prompt(spec, aspect, locale, template_override=None):
    template = load_template(locale, template_override)
    bindings = build_bindings(spec, aspect)

    def substitute(match):
        name = match.group(1)
        if name not in bindings:
            raise SystemExit(f"template variable not bound by shot spec: {name}")
        return bindings[name]

    rendered = re.sub(r"\{\{\s*([a-z_0-9]+)\s*\}\}", substitute, template)
    if "{{" in rendered:
        raise SystemExit("unresolved template variable remains after binding")
    return rendered


def write_outputs(spec, args):
    combo = combo_id(spec, args.aspect)
    tags = compute_tags(spec, args.aspect)
    out = Path(args.out)
    prompts_dir = out / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)

    filename = f"01-{spec['id']}.md"
    (prompts_dir / filename).write_text(
        render_prompt(spec, args.aspect, args.locale, args.template), encoding="utf-8"
    )

    manifest = {
        "schema_version": "precision-candid-shot/1.0",
        "shot": spec["id"],
        "combo": combo,
        "aspect": args.aspect,
        "model": "openai/gpt-5.4-image-2",
        "images": [
            {
                "file": f"prompts/{filename}",
                "combo": combo,
                "tags": tags,
                "palette": spec.get("palette", []),
            }
        ],
    }
    (out / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "schema_version: eikona.batch.v1",
        f'goal: "precision candid shot {spec["id"]}"',
        "defaults:",
        "  kind: image.generate",
        "  model: openai/gpt-5.4-image-2",
        f"  size: {args.size}  # {args.aspect} portrait; adjust per provider",
        "matrix:",
        "  prompt_files:",
        f"    - prompts/{filename}",
        "limits:",
        "  max_jobs: 1",
        "  max_parallel: 1",
        "  allow_unknown_cost: false",
        "  fail_fast: true",
        "policy:",
        "  approval_required: true",
        "",
    ]
    (out / "runbook.yaml").write_text("\n".join(lines), encoding="utf-8")
    print(f"[{combo}] {spec['id']} -> {out}")
    print("tags: " + " / ".join(tags))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--shot", help="shot spec id under assets/shots/")
    parser.add_argument("--aspect", help="override spec aspect, e.g. 9:16")
    parser.add_argument("--locale", default="en", help="template locale: en (default, canonical delivery) or zh-CN")
    parser.add_argument("--template", help="override template path; default from the yeisme-prompt-templates repository")
    parser.add_argument("--size", default="1024x1536")
    parser.add_argument("--out", help="output collection dir; default prompts/generic/precision-candid/<shot>")
    parser.add_argument("--list-shots", action="store_true")
    args = parser.parse_args()

    if args.list_shots:
        for path in sorted(SHOTS_DIR.glob("*.json")):
            print(path.stem)
        return
    if not args.shot:
        parser.error("--shot is required unless --list-shots")

    spec = load_shot(args.shot)
    args.aspect = args.aspect or spec["aspect"]
    if not args.out:
        args.out = str(Path("prompts") / "generic" / "precision-candid" / spec["id"])
    write_outputs(spec, args)


if __name__ == "__main__":
    sys.exit(main())
