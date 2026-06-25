#!/usr/bin/env python3
"""构建 AGENT 七层手册 PDF。

使用 markdown2 → HTML → xhtml2pdf 路线，
无需 pandoc / LaTeX 等外部依赖。
"""
import io
import re
import sys
from pathlib import Path

import markdown2
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from xhtml2pdf import pisa
from xhtml2pdf.default import DEFAULT_FONT

ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = ROOT / "build"
DIST_DIR = BUILD_DIR / "dist"
CSS_PATH = BUILD_DIR / "templates" / "pdf-style.css"

SIMHEI_FONT_PATH = "C:/Windows/Fonts/simhei.ttf"
SIMHEI_FONT_NAME = "SimHei"
FANGSONG_FONT_PATH = "C:/Windows/Fonts/simfang.ttf"
FANGSONG_FONT_NAME = "FangSong"

pdfmetrics.registerFont(TTFont(SIMHEI_FONT_NAME, SIMHEI_FONT_PATH))
pdfmetrics.registerFont(TTFont(FANGSONG_FONT_NAME, FANGSONG_FONT_PATH))
DEFAULT_FONT["microsoft yahei"] = SIMHEI_FONT_NAME
DEFAULT_FONT["simsun"] = SIMHEI_FONT_NAME
DEFAULT_FONT["simhei"] = SIMHEI_FONT_NAME
DEFAULT_FONT["sans-serif"] = SIMHEI_FONT_NAME
DEFAULT_FONT["fangsong"] = FANGSONG_FONT_NAME
DEFAULT_FONT["simfang"] = FANGSONG_FONT_NAME

LAYERS = [
    "l1-theory", "l2-context", "l3-protocol",
    "l4-framework", "l5-pattern", "l6-observability",
    "l7-production-security", "l8-case-studies",
]

APPENDICES = [
    "appendix-a-react-template", "appendix-b-multi-agent-skeleton",
    "appendix-c-framework-matrix", "appendix-d-glossary",
]

QUIZZES = ["quiz-l1-l3", "quiz-l4-l5", "quiz-l6-l8"]


def collect_markdown_files() -> list[Path]:
    """按顺序收集所有 Markdown 文件。"""
    files = []
    readme = ROOT / "README.md"
    if readme.exists():
        files.append(readme)

    for layer in LAYERS:
        layer_dir = ROOT / "handbook" / layer
        if layer_dir.is_dir():
            for md in sorted(layer_dir.glob("*.md")):
                files.append(md)

    appendix_dir = ROOT / "handbook" / "appendices"
    if appendix_dir.is_dir():
        for name in APPENDICES:
            md = appendix_dir / f"{name}.md"
            if md.exists():
                files.append(md)

    if appendix_dir.is_dir():
        for name in QUIZZES:
            md = appendix_dir / f"{name}.md"
            if md.exists():
                files.append(md)

    return files


def md_to_html(md_path: Path) -> str:
    """将单个 Markdown 文件转为 HTML 片段。"""
    text = md_path.read_text(encoding="utf-8")

    text = _replace_status_emoji(text)

    text = re.sub(
        r'```mermaid\n(.*?)```',
        r'<div class="mermaid-placeholder"><p><em>[Mermaid 图 — 请参见在线版本]</em></p></div>',
        text,
        flags=re.DOTALL,
    )

    html = markdown2.markdown(
        text,
        extras=[
            "fenced-code-blocks",
            "tables",
            "header-ids",
            "toc",
            "strike",
            "task_list",
            "smarty-pants",
            "code-friendly",
        ],
    )

    html = _strip_list_bullets(html)
    return html


def _replace_status_emoji(text: str) -> str:
    """把 SimHei 不支持的彩色状态 emoji 替换为几何符号。"""
    return (
        text.replace("🟢", "●")
        .replace("🟡", "▲")
        .replace("🔴", "■")
        .replace("🔵", "●")
        .replace("🟣", "◆")
        .replace("🟠", "▲")
    )


def _strip_list_bullets(html: str) -> str:
    """将 <ul>/<ol>/<li> 替换为 div, 避免 xhtml2pdf 硬编码渲染 ☐ bullet。"""
    html = re.sub(r"<ul[^>]*>", '<div class="mdlist">', html)
    html = re.sub(r"</ul>", "</div>", html)
    html = re.sub(r"<ol[^>]*>", '<div class="mdlist-ol">', html)
    html = re.sub(r"</ol>", "</div>", html)
    html = re.sub(r"<li[^>]*>", '<div class="mditem">', html)
    html = re.sub(r"</li>", "</div>", html)
    return html


def build_pdf() -> bool:
    """构建完整 PDF。"""
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    output_path = DIST_DIR / "AGENT七层手册.pdf"

    md_files = collect_markdown_files()
    print(f"收集到 {len(md_files)} 个 Markdown 文件")

    html_parts = []

    readme_html = md_to_html(md_files[0])
    cover_html = f'<div class="cover">{readme_html}</div>'
    html_parts.append(cover_html)

    index_path = ROOT / "INDEX.md"
    if index_path.exists():
        toc_html = md_to_html(index_path)
        html_parts.append(f'<div class="toc">{toc_html}</div>')

    for md_file in md_files[1:]:
        html_parts.append(md_to_html(md_file))
        print(f"  已转换: {md_file.relative_to(ROOT)}")

    css = CSS_PATH.read_text(encoding="utf-8") if CSS_PATH.exists() else ""

    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<style>
{css}
</style>
</head>
<body>
{"".join(html_parts)}
</body>
</html>"""

    with open(output_path, "wb") as f:
        pdf = pisa.CreatePDF(io.StringIO(full_html), f, encoding="utf-8")

    if pdf.err:
        print(f"PDF 生成有 {pdf.err} 个警告/错误", file=sys.stderr)
    else:
        print(f"PDF 已生成: {output_path}")

    size_mb = output_path.stat().st_size / 1024 / 1024
    print(f"文件大小: {size_mb:.1f} MB")
    return pdf.err == 0


if __name__ == "__main__":
    success = build_pdf()
    sys.exit(0 if success else 1)
