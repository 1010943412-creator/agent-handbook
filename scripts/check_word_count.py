#!/usr/bin/env python3
"""验收：每节 Markdown 字数 800-1500。"""
import sys
import re
from pathlib import Path

def count_words(md_path: Path) -> int:
    text = md_path.read_text(encoding="utf-8")
    # 去除代码块、引用块、图片、链接
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    text = re.sub(r"^>.*$", "", text, flags=re.M)
    # 中文字符 + 英文单词
    cn = len(re.findall(r"[一-鿿]", text))
    en = len(re.findall(r"[a-zA-Z]+", text))
    return cn + en

def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python check_word_count.py <dir>")
        return 1
    target = Path(sys.argv[1])
    files = list(target.rglob("*.md"))
    if not files:
        print(f"No .md files in {target}")
        return 0
    fail = 0
    for f in files:
        if "INDEX" in f.name or "README" in f.name or "answers" in f.name.lower():
            continue
        n = count_words(f)
        status = "OK" if 800 <= n <= 1500 else "FAIL"
        if status == "FAIL":
            fail += 1
        print(f"[{status}] {f.relative_to(target)}: {n} 字")
    print(f"\n共 {len(files)} 个 .md, 失败 {fail} 个")
    return 0 if fail == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
