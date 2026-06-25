"""增量更新 AGENT 七层手册 PDF 封面页邮箱。

策略: PyMuPDF 文本替换 (surgery)
- 打开原 PDF
- 在第 1 页 (封面) 定位 "qingnuan@local"
- 用 redaction API 删除旧文字 + 子集化 SimHei 嵌入新文字
- saveIncr 增量保存 (只追加, 不重写)

为什么快:
- 不重新跑 Chrome headless (省 5-10 分钟)
- 不重新解析 95 个 Markdown
- 不重新请求 mermaid.ink
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import fitz  # PyMuPDF
from fontTools.subset import Subsetter
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "build" / "dist"
PDF = DIST / "AGENT七层手册.pdf"

OLD = "qingnuan@local"
NEW = "1010943412@qq.com"

# 备份原文件 (首次执行时)
BACKUP = DIST / "AGENT七层手册.bak.pdf"


def _subset_font_to_chars(ttf_path: Path, chars: str) -> bytes:
    """从 TTF 中只保留 chars 字符的 glyph, 返回子集 buffer。"""
    font = TTFont(str(ttf_path))
    subsetter = Subsetter()
    subsetter.populate(text=chars)
    subsetter.subset(font)
    buf = io.BytesIO()
    font.save(buf)
    return buf.getvalue()


def main() -> int:
    if not PDF.exists():
        print(f"ERROR: {PDF} 不存在")
        return 1

    if not BACKUP.exists():
        BACKUP.write_bytes(PDF.read_bytes())
        print(f"已备份: {BACKUP}")

    doc = fitz.open(str(PDF))
    cover = doc[0]

    instances = cover.search_for(OLD)
    print(f"封面页找到 {len(instances)} 处 '{OLD}'")

    if not instances:
        print("未找到旧邮箱，未修改文件")
        return 1

    # Step 1: 用 redaction API 彻底删除旧文字 (从内容流中真正移除)
    for rect in instances:
        cover.add_redact_annot(rect, fill=(1, 1, 1))
    cover.apply_redactions()

    # Step 2: 探测嵌入字体 (用于回退方案)
    fonts = cover.get_fonts(full=True)
    font_xref = None
    for f in fonts:
        xref, ext, ftype, basefont, name = f[0], f[1], f[2], f[3], f[4]
        if "MicrosoftYaHei" in (basefont or "") and "Bold" not in (basefont or ""):
            font_xref = xref
            print(f"参考字体: {basefont} (xref={xref})")
            break

    # Step 3: 用 insert_htmlbox 写入新邮箱
    # MuPDF HTML/CSS 引擎会查找系统字体 (SimHei/YaHei), 视觉与正文一致
    for rect in instances:
        cover.insert_htmlbox(
            rect,
            f'<span style="font-family:SimHei,Microsoft YaHei,sans-serif;font-size:10.5pt;color:#1a1a1a">{NEW}</span>',
        )

    # 增量保存 (只追加变更, 不重写整个 PDF, 1-2 秒完成)
    doc.saveIncr()
    doc.close()

    size_mb = PDF.stat().st_size / 1024 / 1024
    print(f"已更新: {PDF} ({size_mb:.2f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
