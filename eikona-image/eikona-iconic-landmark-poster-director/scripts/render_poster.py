#!/usr/bin/env python3
"""Render an ICONIC LANDMARK SERIES poster prompt from a city spec.

The visual system (45/55 photo/vector split, archival typography, style stack,
negative prompt) is fixed in this renderer; only the city spec varies. Writes
the prompt file, manifest.json (namespaced tags) and runbook.yaml following
the eikona-file-prompt-workflow prompt library convention, and can regenerate
the series index from assets/cities/*.json.

Examples:
  python3 render_poster.py --city london \
      --out prompts/generic/landmark-poster/london
  python3 render_poster.py --reindex
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
CITIES_DIR = SKILL_ROOT / "assets" / "cities"
SERIES_INDEX = SKILL_ROOT / "assets" / "series-index.json"

STYLE_STACK = (
    "Swiss International Style + British modernism + Bauhaus + Mid-century travel poster "
    "+ architectural editorial illustration + museum exhibition graphic design "
    "+ Japanese minimalism + Scandinavian graphic design"
)

NEGATIVE_BASE = [
    "赛博朋克", "未来城市", "3D渲染", "黏土风", "油画", "水彩", "粗黑描边",
    "过度饱和", "强HDR", "建筑透视错误", "密集游客", "大量汽车", "杂乱背景", "文字乱码",
]


def load_city(city_id):
    path = CITIES_DIR / f"{city_id}.json"
    if not path.exists():
        raise SystemExit(f"unknown city: {city_id} (looked for {path})")
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def combo_id(city, aspect):
    raw = json.dumps(city, ensure_ascii=False, sort_keys=True) + f"|{aspect}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:8]


def compute_tags(city, aspect):
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
    return tags


def render_prompt(city, aspect):
    p, v, t = city["photo"], city["vector"], city["typography"]
    hero = next(lm for lm in city["landmarks"] if lm["role"] == "hero")
    supporting = [lm["name"] for lm in city["landmarks"] if lm["role"] == "supporting"]
    foreground = [lm["name"] for lm in city["landmarks"] if lm["role"] == "foreground"]
    coords = "\n".join(city["city"]["coordinates"])
    negatives = "、".join(NEGATIVE_BASE + city.get("negative_extra", []))

    return f"""# ICONIC LANDMARK SERIES No.{city['series']['no']:03d} — {city['city']['name']}

创建一张竖版 {aspect} 高级城市地标建筑艺术海报，主题为{city['city']['name']}，核心地标为 {' + '.join(lm['name'] for lm in city['landmarks'])}。

延续统一的 ICONIC LANDMARK SERIES 视觉系统：上半部分真实城市摄影 + 下半部分极简二维矢量建筑解构插画。上下两部分必须表现同一组地标，并具有明显的视觉对应关系。

## 上半部分｜真实摄影（约占 45%）

{p['viewpoint']}。
{p['hero_placement']}。
清晰表现标志性的：{'、'.join(p['hero_features'])}。
{p['skyline']}。
{p['river']}。
{p['scale_reference']}。
{p['background']}。
时间设定：{p['time']}。天空形成{p['sky_gradient']}。{p['clouds']}。{p['rim_light']}。
{p['lens']}。
{p['quality']}。

## 下半部分｜建筑矢量解构（约占 55%）

背景转换成温暖象牙白、奶油白高级艺术纸张，大面积干净负空间。将上半部分真实建筑重新设计成极简二维建筑矢量插画。{hero['name']} 仍位于视觉中心偏右，与上方真实摄影保持相似视觉轴线。

必须严格保留最核心的识别元素：{'、'.join(v['hero_identity'])}。
{v['hero_simplification']}。
主体使用：{'、'.join(v['hero_palette'])}。

{v['supporting']}。使用低饱和：{'、'.join(v['supporting_palette'])}。

{v['sun']}。

{v['river']}。
{v['easter_egg']}。
{v['feel']}。

## Typography｜建筑档案排版

左下方使用大写英文：

{t['title'][0]}

第二行：

{t['title'][1]}

使用高级现代主义无衬线字体，细字重，明显增加字母间距。主标题使用深海军蓝 / Charcoal Navy。下方极细短横线。小字号：{t['subtitle']}。

左上角极小字号：

ICONIC
LANDMARK
SERIES

—

No.{city['series']['no']:03d}

右上角：

EST.
{city['city']['est']}

右下角：

{coords}

最下方极小字号：{t['footer']}。

所有字体遵循建筑事务所档案、博物馆展览图录式排版。

## 最终风格

{STYLE_STACK}。

温暖象牙白纸张，大面积留白，精准网格系统，超细线条，低饱和莫兰迪配色，建筑比例准确。上半真实摄影，下半二维矢量解构，上下地标严格对应。高级、克制、安静、建筑杂志感、博物馆收藏海报质感。4K，ultra clean vector edges，premium print design，museum quality，collector's architectural poster。

## 负面提示词

{negatives}。
"""


def write_outputs(city, args):
    combo = combo_id(city, args.aspect)
    tags = compute_tags(city, args.aspect)
    out = Path(args.out)
    prompts_dir = out / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)

    hero = next(lm for lm in city["landmarks"] if lm["role"] == "hero")
    filename = f"01-{city['id']}-{hero['id']}.md"
    (prompts_dir / filename).write_text(
        render_prompt(city, args.aspect), encoding="utf-8"
    )

    manifest = {
        "schema_version": "iconic-landmark-poster/1.0",
        "city": city["id"],
        "series": city["series"],
        "combo": combo,
        "aspect": args.aspect,
        "model": "openai/gpt-5.4-image-2",
        "images": [
            {"file": f"prompts/{filename}", "combo": combo, "tags": tags}
        ],
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
    print(f"[{combo}] {city['city']['name']} -> {out}")
    print("tags: " + " / ".join(tags))


def reindex():
    posters = []
    for path in sorted(CITIES_DIR.glob("*.json")):
        with path.open(encoding="utf-8") as f:
            city = json.load(f)
        posters.append(
            {
                "no": city["series"]["no"],
                "city": city["id"],
                "name": city["city"]["name"],
                "landmarks": [lm["id"] for lm in city["landmarks"]],
                "spec": f"cities/{path.name}",
                "combo": combo_id(city, "2:3"),
            }
        )
    posters.sort(key=lambda p: p["no"])
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
