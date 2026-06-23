#!/usr/bin/env python3
"""验收：每节末尾引用块 ≥ 3 条 S/A 级。"""
import sys
import re
from pathlib import Path

# 同目录的 S/A 域名 & 作者清单
sys.path.insert(0, str(Path(__file__).parent))
from _reference_domains import S_A_DOMAINS, KEY_AUTHORS  # noqa: E402

# P9 例外:附录 D 纯术语 + 3 个题库,spec 明确 0 引用
REF_EXEMPT = (
    "appendix-d-glossary.md",
    "quiz-l1-l3.md",
    "quiz-l4-l5.md",
    "quiz-l6-l8.md",
)


def count_refs(md_path: Path) -> int:
    """统计"📚 / 本节参考"小节中 S/A 级引用条数。

    识别策略：
    - 找到 "📚" 或 "本节参考" 起始位置
    - 截取从该位置到下一个 ## 标题或文件末尾之间的内容
    - 提取所有 `> - ...` / `> * ...` 形式的引用条目
    - 包含 S/A 域名或知名作者署名则计 1
    """
    text = md_path.read_text(encoding="utf-8")
    ref_start = max(text.find("📚"), text.find("本节参考"))
    if ref_start < 0:
        return 0

    ref_section = text[ref_start:]

    # 找到下一个二级标题（## 开头）作为本节结束
    next_heading = re.search(r"^##\s", ref_section, re.M)
    if next_heading:
        ref_section = ref_section[: next_heading.start()]

    # 提取所有引用条目行
    ref_lines = re.findall(r"^>\s*[-*]\s*(.+)$", ref_section, re.M)

    count = 0
    for line in ref_lines:
        if any(d in line for d in S_A_DOMAINS):
            count += 1
        elif any(a in line for a in KEY_AUTHORS):
            count += 1
    return count


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python check_references.py <dir>")
        return 1
    target = Path(sys.argv[1])
    files = list(target.rglob("*.md"))
    fail = 0
    for f in files:
        if any(k in f.name for k in ["INDEX", "README", "answers"]):
            continue
        if f.name in REF_EXEMPT:
            print(f"[SKIP] {f.relative_to(target)}: 豁免(spec 明确 0 引用)")
            continue
        n = count_refs(f)
        status = "OK" if n >= 3 else "FAIL"
        if status == "FAIL":
            fail += 1
        print(f"[{status}] {f.relative_to(target)}: {n} 条 S/A 级引用")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
