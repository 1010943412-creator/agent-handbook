#!/usr/bin/env python3
"""验收：每节 ≥ 1 张图（统计 ![]() 与 mermaid 代码块）。"""
import sys
import re
from pathlib import Path

def count_figs(md_path: Path) -> int:
    text = md_path.read_text(encoding="utf-8")
    img = len(re.findall(r"!\[.*?\]\(.*?\)", text))
    mermaid = len(re.findall(r"^```mermaid\s*$", text, re.M))
    return img + mermaid

def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python check_figures.py <dir>")
        return 1
    target = Path(sys.argv[1])
    files = list(target.rglob("*.md"))
    fail = 0
    for f in files:
        if any(k in f.name for k in ["INDEX", "README", "answers"]):
            continue
        n = count_figs(f)
        status = "OK" if n >= 1 else "FAIL"
        if status == "FAIL":
            fail += 1
        print(f"[{status}] {f.relative_to(target)}: {n} 张图")
    return 0 if fail == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
