#!/usr/bin/env python3
"""Render an ICONIC LANDMARK SERIES poster prompt from a city spec.

The canonical prompt template lives in the prompt repository
(data/yeisme-prompt-templates/solutions/image/iconic-landmark-poster); this
renderer loads it and binds the city spec JSON to its {{variables}}. City
specs, variant merging, series index, tags, and runbook/manifest generation
stay here. Variants deep-merge over the base spec (dicts merge recursively,
lists/scalars replace, negative_extra appends).

Examples:
  python3 render_poster.py --city london \
      --out prompts/generic/landmark-poster/london
  python3 render_poster.py --reindex
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
CITIES_DIR = SKILL_ROOT / "assets" / "cities"
SERIES_INDEX = SKILL_ROOT / "assets" / "series-index.json"
SOLUTION_ID = "iconic-landmark-poster"


def load_city(city_id):
    path = CITIES_DIR / f"{city_id}.json"
    if not path.exists():
        raise SystemExit(f"unknown city: {city_id} (looked for {path})")
    with path.open(encoding="utf-8") as f:
        return json.load(f)


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


def deep_merge(base, overrides):
    merged = dict(base)
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        elif key == "negative_extra" and isinstance(value, list):
            merged[key] = list(merged.get(key, [])) + value
        else:
            merged[key] = value
    return merged


def expand_variants(city):
    base = {k: v for k, v in city.items() if k != "variants"}
    posters = [("base", None, base)]
    for variant in city.get("variants", []):
        merged = deep_merge(base, variant.get("overrides", {}))
        posters.append((variant["id"], variant.get("label"), merged))
    return posters


def combo_id(spec, aspect, variant=None):
    raw = json.dumps(spec, ensure_ascii=False, sort_keys=True) + f"|{aspect}"
    if variant:
        raw += f"|{variant}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:8]


def compute_tags(city, aspect, variant=None):
    palette = city["tags"]["palette"]
    tags = [
        f"series:{city['series']['id']}",
        f"series.no:{city['series']['no']:03d}",
        f"geo.city:{city['id']}",
        f"geo.country:{city['city']['country'].lower().replace(' ', '-')}",
        "layout:photo-vector-split",
        f"aspect:{aspect}",
        f"palette.family:{palette['family']}",
        f"palette.paper:{palette['paper']}",
        "component:photography",
        "component:vector-deconstruction",
        "component:archival-typography",
    ]
    tags += [f"landmark:{lm['id']}" for lm in city["landmarks"]]
    tags += [f"palette.accent:{a}" for a in palette["accents"]]
    tags += [f"use:{u}" for u in city["tags"]["use"]]
    tags.append(f"variant:{variant or 'base'}")
    return tags


def build_bindings(city, aspect):
    p, v, t = city["photo"], city["vector"], city["typography"]
    return {
        "city_name": city["city"]["name"],
        "landmarks_line": " + ".join(lm["name"] for lm in city["landmarks"]),
        "series_no": f"{city['series']['no']:03d}",
        "aspect": aspect,
        "viewpoint": p["viewpoint"],
        "hero_placement": p["hero_placement"],
        "hero_features": "、".join(p["hero_features"]),
        "skyline": p["skyline"],
        "river": p["river"],
        "scale_reference": p["scale_reference"],
        "background": p["background"],
        "time": p["time"],
        "sky_gradient": p["sky_gradient"],
        "clouds": p["clouds"],
        "rim_light": p["rim_light"],
        "lens": p["lens"],
        "quality": p["quality"],
        "hero_identity": "、".join(v["hero_identity"]),
        "hero_simplification": v["hero_simplification"],
        "hero_palette": "、".join(v["hero_palette"]),
        "supporting": v["supporting"],
        "supporting_palette": "、".join(v["supporting_palette"]),
        "sun": v["sun"],
        "river_lines": v["river"],
        "easter_egg": v["easter_egg"],
        "feel": v["feel"],
        "title_line1": t["title"][0],
        "title_line2": t["title"][1],
        "subtitle": t["subtitle"],
        "est": city["city"]["est"],
        "coordinates": "\n".join(city["city"]["coordinates"]),
        "footer": t["footer"],
        "negative_extra": "、".join(city.get("negative_extra", [])) or "无额外负面项",
    }


def render_prompt(city, aspect, locale, template_override=None):
    template = load_template(locale, template_override)
    bindings = build_bindings(city, aspect)

    def substitute(match):
        name = match.group(1)
        if name not in bindings:
            raise SystemExit(f"template variable not bound by city spec: {name}")
        return bindings[name]

    rendered = re.sub(r"\{\{\s*([a-z_0-9]+)\s*\}\}", substitute, template)
    if "{{" in rendered:
        raise SystemExit("unresolved template variable remains after binding")
    return rendered


def write_outputs(city, args):
    out = Path(args.out)
    prompts_dir = out / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)

    posters = expand_variants(city)
    prompt_files, images = [], []
    for i, (variant_id, variant_label, spec) in enumerate(posters, start=1):
        combo = combo_id(spec, args.aspect, variant=variant_id)
        tags = compute_tags(spec, args.aspect, variant=variant_id)
        hero = next(lm for lm in spec["landmarks"] if lm["role"] == "hero")
        suffix = f"-{variant_id}" if variant_id != "base" else ""
        filename = f"{i:02d}-{city['id']}-{hero['id']}{suffix}.md"
        (prompts_dir / filename).write_text(
            render_prompt(spec, args.aspect, args.locale, args.template), encoding="utf-8"
        )
        prompt_files.append(f"prompts/{filename}")
        images.append(
            {
                "file": f"prompts/{filename}",
                "variant": variant_id,
                "label": variant_label,
                "combo": combo,
                "tags": tags,
            }
        )
        print(f"[{combo}] {variant_id}: {filename}")

    manifest = {
        "schema_version": "iconic-landmark-poster/1.1",
        "city": city["id"],
        "series": city["series"],
        "aspect": args.aspect,
        "locale": args.locale,
        "model": "openai/gpt-5.4-image-2",
        "images": images,
    }
    (out / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "schema_version: eikona.batch.v1",
        f'goal: "ICONIC LANDMARK SERIES No.{city["series"]["no"]:03d} {city["city"]["name"]} poster"',
        "defaults:",
        "  kind: image.generate",
        "  model: openai/gpt-5.4-image-2",
        f"  size: {args.size}  # {args.aspect} portrait; adjust per provider",
        "matrix:",
        "  prompt_files:",
    ]
    lines += [f"    - {p}" for p in prompt_files]
    lines += [
        "limits:",
        f"  max_jobs: {len(prompt_files)}",
        "  max_parallel: 1",
        "  allow_unknown_cost: false",
        "  fail_fast: true",
        "policy:",
        "  approval_required: true",
        "",
    ]
    (out / "runbook.yaml").write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {len(prompt_files)} prompt(s) + manifest.json + runbook.yaml -> {out}")


def reindex():
    posters = []
    for path in sorted(CITIES_DIR.glob("*.json")):
        with path.open(encoding="utf-8") as f:
            city = json.load(f)
        base = {k: v for k, v in city.items() if k != "variants"}
        posters.append(
            {
                "no": city["series"]["no"],
                "city": city["id"],
                "name": city["city"]["name"],
                "landmarks": [lm["id"] for lm in city["landmarks"]],
                "variants": ["base"] + [v["id"] for v in city.get("variants", [])],
                "spec": f"cities/{path.name}",
                "combo": combo_id(base, "2:3"),
            }
        )
    posters.sort(key=lambda p: p["no"])
    numbers = [p["no"] for p in posters]
    if len(numbers) != len(set(numbers)):
        raise SystemExit(f"duplicate series.no in city specs: {sorted(numbers)}")
    index = {
        "schema_version": "iconic-landmark-series/1.0",
        "series": "iconic-landmark",
        "posters": posters,
    }
    SERIES_INDEX.write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"series index: {len(posters)} poster(s) -> {SERIES_INDEX}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--city", help="city spec id under assets/cities/")
    parser.add_argument("--aspect", default="2:3")
    parser.add_argument("--size", default="1024x1536")
    parser.add_argument("--locale", default="en", help="template locale: en (default, compile/delivery); zh-CN is a human-review translation only")
    parser.add_argument("--template", help="override template path; default from the yeisme-prompt-templates repository")
    parser.add_argument("--out", help="output collection dir; default prompts/generic/landmark-poster/<city>")
    parser.add_argument("--reindex", action="store_true", help="regenerate assets/series-index.json")
    parser.add_argument("--list-cities", action="store_true")
    args = parser.parse_args()

    if args.list_cities:
        for path in sorted(CITIES_DIR.glob("*.json")):
            print(path.stem)
        return
    if args.reindex:
        reindex()
        return
    if not args.city:
        parser.error("--city is required unless --reindex/--list-cities")

    city = load_city(args.city)
    if not args.out:
        args.out = str(Path("prompts") / "generic" / "landmark-poster" / city["id"])
    write_outputs(city, args)


if __name__ == "__main__":
    sys.exit(main())
