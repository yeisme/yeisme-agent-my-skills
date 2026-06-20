#!/usr/bin/env python3
import re
import sys
from pathlib import Path


def chinese_count(text: str) -> int:
    text = re.sub(r"#{1,6}\s*", "", text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    text = re.sub(r'[`*_~>"]', "", text)
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_chinese_chapter_wordcount.py <chapter.md|directory> [min_chars]", file=sys.stderr)
        return 2
    target = Path(sys.argv[1])
    min_chars = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    files = sorted(target.glob("第*.md")) if target.is_dir() else [target]
    if not files:
        print(f"status=failed reason=no_chapter_files target={target}")
        return 1
    failed = 0
    total = 0
    for file in files:
        if not file.exists():
            print(f"file={file} status=failed reason=missing")
            failed += 1
            continue
        count = chinese_count(file.read_text(encoding="utf-8"))
        total += count
        status = "pass" if count >= min_chars else "failed"
        if status == "failed":
            failed += 1
        print(f"file={file} status={status} chinese_chars={count} min_chars={min_chars}")
    print(f"summary files={len(files)} failed={failed} total_chinese_chars={total}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
