#!/usr/bin/env python3
"""验收：L8 案例 ≥ 2 张图（mermaid 代码块为主，markdown 图片为辅）。

基于 check_figures.py 的 count_figs() 复用，阈值改为 2。
"""
import sys
import re
from pathlib import Path
from check_figures import count_figs

CASE_FIG_MIN = 2
EXCLUDE = ("INDEX", "README", "answers")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python check_case_figures.py <dir>")
        return 1
    target = Path(sys.argv[1])
    files = [f for f in target.rglob("*.md")
             if not any(k in f.name for k in EXCLUDE)]
    if not files:
        print(f"No case .md files in {target}")
        return 0
    fail = 0
    for f in files:
        n = count_figs(f)
        status = "OK" if n >= CASE_FIG_MIN else "FAIL"
        if status == "FAIL":
            fail += 1
        print(f"[{status}] {f.relative_to(target)}: {n} 张图")
    print(f"\n共 {len(files)} 个案例 .md, 失败 {fail} 个")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())