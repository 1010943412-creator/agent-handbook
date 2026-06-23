#!/usr/bin/env python3
"""验收：L8 案例字数 1200-2500。

字数口径："中文字符 1 计 1，英文单词 1 计 1"。
基于 check_word_count.py 的 count_text_units() 复用。
"""
import sys
import re
import unicodedata
from pathlib import Path
from check_word_count import count_text_units

CASE_WORD_MIN = 1200
CASE_WORD_MAX = 2500
EXCLUDE = ("INDEX", "README", "answers")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python check_case_word_count.py <dir>")
        return 1
    target = Path(sys.argv[1])
    files = [f for f in target.rglob("*.md")
             if not any(k in f.name for k in EXCLUDE)]
    if not files:
        print(f"No case .md files in {target}")
        return 0
    fail = 0
    for f in files:
        n = count_text_units(f)
        status = "OK" if CASE_WORD_MIN <= n <= CASE_WORD_MAX else "FAIL"
        if status == "FAIL":
            fail += 1
        print(f"[{status}] {f.relative_to(target)}: {n} 字")
    print(f"\n共 {len(files)} 个案例 .md, 失败 {fail} 个")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())