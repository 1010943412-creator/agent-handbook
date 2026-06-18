#!/usr/bin/env python3
"""验收：每节末尾引用块 ≥ 3 条 S/A 级。"""
import sys
import re
from pathlib import Path

S_A_DOMAINS = [
    "anthropic.com", "openai.com", "langchain.com", "lilianweng.github.io",
    "eugeneyan.com", "arxiv.org", "github.com", "deepmind.google",
    "huggingface.co", "docs.anthropic.com", "platform.openai.com",
]

def count_refs(md_path: Path) -> int:
    text = md_path.read_text(encoding="utf-8")
    in_ref = False
    count = 0
    for line in text.split("\n"):
        if "本节参考" in line or "📚" in line:
            in_ref = True
            continue
        if in_ref:
            if line.startswith("> -") or line.startswith("> *"):
                if any(d in line for d in S_A_DOMAINS) or "Lilian" in line or "Eugene" in line:
                    count += 1
            elif line.startswith("#"):
                in_ref = False
    return count

def main() -> int:
    target = Path(sys.argv[1])
    files = list(target.rglob("*.md"))
    fail = 0
    for f in files:
        if any(k in f.name for k in ["INDEX", "README", "answers"]):
            continue
        n = count_refs(f)
        status = "OK" if n >= 3 else "FAIL"
        if status == "FAIL":
            fail += 1
        print(f"[{status}] {f.relative_to(target)}: {n} 条 S/A 级引用")
    return 0 if fail == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
