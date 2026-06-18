#!/usr/bin/env python3
"""验收：每节 Markdown 字数 800-1500。

字数口径："中文字符 1 计 1，英文单词 1 计 1"。
- 中文字符：Unicode CJK 块（含 CJK 统一汉字、CJK 统一汉字扩展 A-G、兼容汉字等）
- 英文单词：连续的 a-zA-Z 序列
"""
import sys
import re
import unicodedata
from pathlib import Path

# 匹配独立的 mermaid / 代码块围栏（避免后续正则误伤）
_FENCE_RE = re.compile(r"^```[a-zA-Z0-9_]*\s*$", re.M)


def count_text_units(md_path: Path) -> int:
    """统计单个 Markdown 文件的"文本单元"数。

    中文字符 1 计 1，英文单词 1 计 1。
    剥离策略：先去除 YAML frontmatter，再去除代码块、引用块、图片、链接。
    """
    text = md_path.read_text(encoding="utf-8")
    # 1) 剥离 YAML frontmatter
    text = re.sub(r"^---\n[\s\S]*?\n---\n", "", text, count=1)
    # 2) 去除代码块、引用块、图片、链接
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    text = re.sub(r"^>.*$", "", text, flags=re.M)
    # 3) 中文字符：使用 unicodedata，覆盖完整 CJK 块
    cn = sum(1 for c in text if "CJK" in unicodedata.name(c, ""))
    # 4) 英文单词
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
        n = count_text_units(f)
        status = "OK" if 800 <= n <= 1500 else "FAIL"
        if status == "FAIL":
            fail += 1
        print(f"[{status}] {f.relative_to(target)}: {n} 字")
    print(f"\n共 {len(files)} 个 .md, 失败 {fail} 个")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
