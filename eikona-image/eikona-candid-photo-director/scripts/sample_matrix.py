#!/usr/bin/env python3
"""Sample candid-photography prompt combinations from matrix.json.

Deterministic: the same --seed/--n/--lock/--exclude inputs always produce the
same batch. Writes prompt files, manifest.json (tags) and runbook.yaml
following the eikona-file-prompt-workflow prompt library convention.

Examples:
  python3 sample_matrix.py --batch summer-01 --seed 42 \
      --out prompts/generic/candid-portrait/summer-01
  python3 sample_matrix.py --batch lotus-01 --seed 7 --n 10 \
      --lock scene=盛夏荷塘 --exclude palette=深蓝夜色+冷白灯光 --dry-run
"""

import argparse
import hashlib
import json
import random
import sys
from pathlib import Path

DIM_ORDER = [
    "expression", "wardrobe", "scene", "moment", "shot", "lens",
    "camera", "composition", "foreground", "light", "palette", "state",
]

MAX_ATTEMPTS = 4000


def load_matrix():
    path = Path(__file__).resolve().parent / "matrix.json"
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def scene_categories(matrix, scene):
    return [
        cat for cat, scenes in matrix["scene_categories"].items() if scene in scenes
    ]


def requirement_met(matrix, pick, required):
    cats = scene_categories(matrix, pick["scene"])
    for req in required:
        if req in matrix["scene_categories"]:
            if req in cats:
                return True
        elif pick["scene"] == req:
            return True
    return False


def compatible(matrix, pick):
    for dim, mapping in matrix["requires_scene"].items():
        required = mapping.get(pick[dim])
        if required and not requirement_met(matrix, pick, required):
            return False
    palette_rule = matrix["palette_rules"].get(pick["palette"])
    if palette_rule:
        if pick["scene"] not in palette_rule["scenes"]:
            return False
        if pick["light"] not in palette_rule["lights"]:
            return False
    allowed_lenses = matrix["lens_state_rules"].get(pick["state"])
    if allowed_lenses and pick["lens"] not in allowed_lenses:
        return False
    return True


def combo_id(pick):
    raw = "|".join(pick[d] for d in DIM_ORDER)
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:8]


def sample_batch(matrix, n, seed, locks, excludes):
    rng = random.Random(seed)
    pools = {
        dim: [v for v in matrix["dimensions"][dim] if v not in excludes.get(dim, set())]
        for dim in DIM_ORDER
    }
    for dim, value in locks.items():
        if value not in pools[dim]:
            raise SystemExit(f"locked value not available: {dim}={value}")
        pools[dim] = [value]
    for dim, pool in pools.items():
        if not pool:
            raise SystemExit(f"empty pool after excludes: {dim}")

    distinct_dims = [d for d in matrix["batch_distinct_dimensions"] if d not in locks]
    batch, seen_combos = [], set()
    while len(batch) < n:
        pick = None
        for _ in range(MAX_ATTEMPTS):
            candidate = {dim: rng.choice(pool) for dim, pool in pools.items()}
            if not compatible(matrix, candidate):
                continue
            cid = combo_id(candidate)
            if cid in seen_combos:
                continue
            if any(
                candidate[d] == prev[d]
                for prev in batch
                for d in distinct_dims
            ):
                continue
            pick = candidate
            break
        if pick is None:
            raise SystemExit(
                f"could not sample item {len(batch) + 1}: relax locks/excludes or reduce n"
            )
        seen_combos.add(combo_id(pick))
        batch.append(pick)
    return batch


PROMPT_TEMPLATE = """# 候选 {index:02d} — {combo}

## 目标

真实生活摄影抓拍写真，{aspect} 竖幅，现代东方夏日写真，极强摄影质感。

## 主体

{subject}。{wardrobe}穿搭。

## 画面

{scene}。{moment}，{expression}。
{shot}，{lens}，{camera}，{composition}。
前景：{foreground}。前景必须自然侵入画面，形成明显遮挡，不要所有元素都完整展示。
光线：{light}。色彩：{palette}。画面最多保留 3—4 个主要色块，避免五颜六色。
摄影状态：{state}。

## 禁用

不要影楼感，不要商业棚拍，不要标准网红摆拍，不要人物直视镜头，不要常规居中人像，不要复杂道具，不要繁杂背景，不要过度磨皮，不要塑料皮肤。
"""


def render_prompt(pick, index, subject, aspect):
    combo = combo_id(pick)
    body = PROMPT_TEMPLATE.format(
        index=index, combo=combo, aspect=aspect, subject=subject, **pick
    )
    return combo, body


def write_outputs(matrix, batch, args, subject_desc):
    out = Path(args.out)
    prompts_dir = out / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)

    prompt_files, images = [], []
    for i, pick in enumerate(batch, start=1):
        combo, body = render_prompt(pick, i, subject_desc, args.aspect)
        filename = f"{i:02d}-{combo}.md"
        (prompts_dir / filename).write_text(body, encoding="utf-8")
        prompt_files.append(f"prompts/{filename}")
        images.append(
            {
                "file": f"prompts/{filename}",
                "combo": combo,
                "tags": {dim: pick[dim] for dim in DIM_ORDER},
                "tag_list": [f"{dim}:{pick[dim]}" for dim in DIM_ORDER],
            }
        )

    manifest = {
        "schema_version": "candid-photo-batch/1.0",
        "batch": args.batch,
        "seed": args.seed,
        "n": len(batch),
        "aspect": args.aspect,
        "model": matrix["defaults"]["model"],
        "subject": args.subject,
        "locks": args.lock or [],
        "excludes": args.exclude or [],
        "images": images,
    }
    (out / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "schema_version: eikona.batch.v1",
        f'goal: "candid lifestyle photography batch {args.batch}"',
        "defaults:",
        "  kind: image.generate",
        f'  model: {matrix["defaults"]["model"]}',
        f"  size: {args.size}  # closest portrait size for {args.aspect}; adjust per provider",
        "matrix:",
        "  prompt_files:",
    ]
    lines += [f"    - {p}" for p in prompt_files]
    lines += [
        "limits:",
        f"  max_jobs: {len(batch)}",
        "  max_parallel: 1",
        "  allow_unknown_cost: false",
        "  fail_fast: true",
        "policy:",
        "  approval_required: true",
        "",
    ]
    (out / "runbook.yaml").write_text("\n".join(lines), encoding="utf-8")


def print_table(batch):
    for i, pick in enumerate(batch, start=1):
        tags = " / ".join(f"{d}:{pick[d]}" for d in ("scene", "camera", "composition", "light"))
        print(f"{i:02d} [{combo_id(pick)}] {tags}")


def parse_kv(pairs, kind):
    result = {}
    for pair in pairs or []:
        if "=" not in pair:
            raise SystemExit(f"invalid {kind} (expect dim=value): {pair}")
        dim, value = pair.split("=", 1)
        result.setdefault(dim.strip(), set()).add(value.strip())
    return result


def main():
    matrix = load_matrix()
    defaults = matrix["defaults"]
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--batch", required=True, help="collection/batch name")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--n", type=int, default=defaults["n"])
    parser.add_argument("--aspect", default=defaults["aspect"])
    parser.add_argument("--size", default=defaults["size"])
    parser.add_argument("--subject", default=defaults["subject"], help="subject id from matrix.json")
    parser.add_argument("--subject-text", help="inline subject description override")
    parser.add_argument("--lock", action="append", help="pin a dimension, e.g. scene=盛夏荷塘 (repeatable)")
    parser.add_argument("--exclude", action="append", help="ban a value, e.g. palette=深蓝夜色+冷白灯光 (repeatable)")
    parser.add_argument("--out", help="output collection dir; default prompts/generic/<asset_type>/<batch>")
    parser.add_argument("--dry-run", action="store_true", help="print table only, write nothing")
    parser.add_argument("--list-subjects", action="store_true")
    args = parser.parse_args()

    if args.list_subjects:
        for sid, subj in matrix["subjects"].items():
            print(f"{sid}: {subj['label']}")
        return

    if args.subject_text:
        subject_desc = args.subject_text
    else:
        subj = matrix["subjects"].get(args.subject)
        if not subj:
            raise SystemExit(f"unknown subject: {args.subject} (see --list-subjects)")
        subject_desc = subj["description"]

    locks = {k: next(iter(v)) for k, v in parse_kv(args.lock, "lock").items()}
    excludes = parse_kv(args.exclude, "exclude")
    for dim in list(locks) + list(excludes):
        if dim not in DIM_ORDER:
            raise SystemExit(f"unknown dimension: {dim} (valid: {', '.join(DIM_ORDER)})")

    batch = sample_batch(matrix, args.n, args.seed, locks, excludes)
    print_table(batch)

    if args.dry_run:
        return
    if not args.out:
        args.out = str(Path("prompts") / "generic" / defaults["asset_type"] / args.batch)
    write_outputs(matrix, batch, args, subject_desc)
    print(f"wrote {len(batch)} prompts + manifest.json + runbook.yaml -> {args.out}")


if __name__ == "__main__":
    sys.exit(main())
