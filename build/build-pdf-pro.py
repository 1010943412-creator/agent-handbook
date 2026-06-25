"""AGENT 七层手册 — 专业版 PDF 构建脚本。

工具链:
- markdown-it-py: Markdown → HTML
- Pygments: 代码语法高亮 (inline 颜色 span)
- mermaid_renderer: ```mermaid``` 块 → PNG
- Chrome headless: HTML → PDF (真正浏览器渲染, CSS3 全支持)

效果:
- 代码高亮 (vs / monokai / one-dark 等)
- mermaid 真图嵌入
- 页眉页脚 (CSS @page margin boxes)
- 中文字体原生渲染 (Chrome 直接用系统 SimHei / Microsoft YaHei)
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from markdown_it import MarkdownIt
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.lexers.special import TextLexer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
HANDBOOK = PROJECT_ROOT / "handbook"
BUILD = PROJECT_ROOT / "build"
DIST = BUILD / "dist"
CACHE_MERMAID = BUILD / ".mermaid_cache"
IMG_OUT = BUILD / "mermaid_img"

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

PYMENTS_STYLE = "vs"
CODE_FONT = '"Consolas", "FangSong", "Microsoft YaHei", monospace'

CHAPTER_TITLES = {
    "l1-theory": "L1 · 基础理论层",
    "l2-context": "L2 · 上下文工程层",
    "l3-protocol": "L3 · 协议与接口层",
    "l4-framework": "L4 · 框架与运行时层",
    "l5-pattern": "L5 · 设计模式层",
    "l6-observability": "L6 · 可观测与评估层",
    "l7-production-security": "L7 · 生产化与安全层",
    "l8-case-studies": "L8 · 实战案例层",
}


# ---------- Markdown 渲染 ----------

def _highlight_code(code: str, lang: str) -> str:
    try:
        lexer = get_lexer_by_name(lang)
    except Exception:
        lexer = TextLexer()
    formatter = HtmlFormatter(style=PYMENTS_STYLE, cssclass="highlight", nobackground=False)
    return highlight(code, lexer, formatter)


def _build_markdown() -> MarkdownIt:
    md = MarkdownIt(
        "gfm-like",
        {
            "html": True,
            "typographer": True,
            "breaks": False,
            "highlight": lambda code, lang, attrs: _highlight_code(code, lang),
        },
    )
    md.enable(["table", "strikethrough"])
    return md


# ---------- Mermaid 渲染 ----------

MERMAID_RE = re.compile(r"```mermaid\n(.*?)```", re.DOTALL)


def _render_mermaid_blocks(md_text: str) -> str:
    """```mermaid...``` → <img src="...png"> 调用 mermaid.ink 在线渲染。"""
    IMG_OUT.mkdir(parents=True, exist_ok=True)
    CACHE_MERMAID.mkdir(parents=True, exist_ok=True)

    def _replace(match: re.Match) -> str:
        import base64, hashlib
        code = match.group(1).strip()
        idx = hashlib.md5(code.encode()).hexdigest()[:10]
        img_path = IMG_OUT / f"m_{idx}.png"
        cache_path = CACHE_MERMAID / f"{idx}.png"

        if not img_path.exists():
            if cache_path.exists():
                img_path.write_bytes(cache_path.read_bytes())
            else:
                try:
                    encoded = base64.urlsafe_b64encode(code.encode("utf-8")).decode("ascii")
                    url = f"https://mermaid.ink/img/{encoded}"
                    req_urlopen = __import__("urllib.request", fromlist=["urlopen"]).urlopen
                    req_Request = __import__("urllib.request", fromlist=["Request"]).Request
                    req = req_Request(url, headers={"User-Agent": "agent-handbook/1.0"})
                    data = req_urlopen(req, timeout=30).read()
                    img_path.write_bytes(data)
                    cache_path.write_bytes(data)
                except Exception as e:
                    print(f"WARN mermaid {idx}: {e}", file=sys.stderr)
                    return f'<div class="mermaid-error"><p>[Mermaid 渲染失败: {e}]</p><pre>{code[:300]}</pre></div>'

        rel = img_path.resolve().as_uri()
        return f'<p class="mermaid"><img src="{rel}" alt="mermaid diagram" /></p>'

    return MERMAID_RE.sub(_replace, md_text)


# ---------- 文件收集 ----------

def _collect_files() -> list[tuple[Path, str, str]]:
    """返回 (md_path, layer, title) 列表，按目录顺序。"""
    files: list[tuple[Path, str, str]] = []

    readme = PROJECT_ROOT / "README.md"
    if readme.exists():
        files.append((readme, "前言", "README"))

    for layer in LAYERS:
        layer_dir = HANDBOOK / layer
        if not layer_dir.is_dir():
            continue
        for md in sorted(layer_dir.glob("*.md")):
            title = "章首页" if md.name == "README.md" else md.stem
            files.append((md, layer, title))

    appendix_dir = HANDBOOK / "appendices"
    if appendix_dir.is_dir():
        for name in APPENDICES + QUIZZES:
            md = appendix_dir / f"{name}.md"
            if md.exists():
                files.append((md, "附录", name))

    return files


def _replace_status_emoji(text: str) -> str:
    """彩色 emoji 在大多数字体下显示为方块, 替换为通用几何符号。"""
    return (
        text.replace("🟢", "●")
        .replace("🟡", "▲")
        .replace("🔴", "■")
        .replace("🔵", "●")
        .replace("🟣", "◆")
        .replace("🟠", "▲")
    )


def _file_to_html(md: MarkdownIt, md_path: Path, layer: str, title: str) -> str:
    raw = md_path.read_text(encoding="utf-8")
    raw = _replace_status_emoji(raw)
    raw = _render_mermaid_blocks(raw)

    chapter_label = CHAPTER_TITLES.get(layer, layer)
    body = md.render(raw)

    page_class = ""
    if "appendix" in md_path.parts or md_path.parent.name == "appendices":
        page_class = "page-appendix"
    elif md_path.name == "README.md":
        page_class = "page-frontmatter"
    else:
        page_class = f"page-{layer}"

    return (
        f'<section class="{page_class}" '
        f'data-chapter="{chapter_label}" data-title="{title}">'
        f'{body}</section>'
    )


# ---------- CSS 模板 ----------

CSS_TEMPLATE = """
@charset "UTF-8";

/* ---------- Pygments {style} 主题 ---------- */
{pygments_css}

/* ---------- 基础排版 ---------- */
* {{ box-sizing: border-box; }}

html, body {{
    margin: 0;
    padding: 0;
    font-family: "Microsoft YaHei", "PingFang SC", "Hiragino Sans GB", "SimSun", sans-serif;
    font-size: 10.5pt;
    line-height: 1.75;
    color: #1a1a1a;
    background: white;
}}

/* ---------- 章节首页 ---------- */
section.page-frontmatter h1 {{
    font-size: 32pt;
    text-align: center;
    margin: 120px 0 30px 0;
    color: #0d1b2a;
    border: none;
}}

section.page-frontmatter blockquote {{
    text-align: center;
    border: none;
    background: transparent;
    font-size: 11pt;
    color: #5fa8d3;
    margin: 20px 0;
}}

/* ---------- 标题 ---------- */
h1 {{
    font-size: 22pt;
    color: #0d1b2a;
    border-bottom: 3px solid #1b4965;
    padding-bottom: 10px;
    margin-top: 30px;
    page-break-after: avoid;
}}

h2 {{
    font-size: 16pt;
    color: #1b4965;
    margin-top: 32px;
    padding-left: 12px;
    border-left: 5px solid #5fa8d3;
    page-break-after: avoid;
}}

h3 {{
    font-size: 13pt;
    color: #2c5f7c;
    margin-top: 24px;
    page-break-after: avoid;
}}

h4 {{
    font-size: 11.5pt;
    color: #5fa8d3;
    margin-top: 20px;
    page-break-after: avoid;
}}

/* ---------- 段落 / 强调 ---------- */
p {{ margin: 10px 0; }}

strong {{ color: #0d1b2a; font-weight: 700; }}
em {{ color: #5c6b73; }}

a {{ color: #1b4965; text-decoration: none; }}

/* ---------- 列表 ---------- */
ul, ol {{ margin: 8px 0; padding-left: 28px; }}

ul li {{ list-style: disc; margin: 4px 0; }}
ul li li {{ list-style: circle; }}
ol li {{ list-style: decimal; margin: 4px 0; }}

/* ---------- 引用 ---------- */
blockquote {{
    border-left: 4px solid #5fa8d3;
    background: linear-gradient(to right, #f0f4f8 0%, #ffffff 100%);
    margin: 16px 0;
    padding: 12px 18px;
    color: #333;
    border-radius: 0 4px 4px 0;
    page-break-inside: avoid;
}}

blockquote p {{ margin: 4px 0; }}

/* ---------- 代码 ---------- */
code {{
    font-family: {code_font};
    font-size: 9.5pt;
    background-color: #f0f0f0;
    padding: 1px 5px;
    border-radius: 3px;
    color: #c7254e;
}}

pre.highlight {{
    font-family: {code_font};
    background-color: #f8f9fa;
    border: 1px solid #e1e4e8;
    border-left: 4px solid #5fa8d3;
    border-radius: 0 4px 4px 0;
    padding: 14px 16px;
    overflow-x: auto;
    font-size: 9pt;
    line-height: 1.55;
    margin: 14px 0;
    page-break-inside: avoid;
}}

pre.highlight code {{
    background: transparent;
    padding: 0;
    color: inherit;
    font-size: inherit;
    border-radius: 0;
}}

/* ---------- 表格 ---------- */
table {{
    border-collapse: collapse;
    width: 100%;
    margin: 16px 0;
    font-size: 10pt;
    page-break-inside: avoid;
}}

th, td {{
    border: 1px solid #d0d7de;
    padding: 8px 12px;
    text-align: left;
    vertical-align: top;
}}

th {{
    background: linear-gradient(to bottom, #1b4965 0%, #16456a 100%);
    color: white;
    font-weight: 700;
    border-color: #0d1b2a;
}}

tr:nth-child(even) {{ background-color: #f6f8fa; }}
tr:hover {{ background-color: #eaf2f8; }}

/* ---------- Mermaid 图片 ---------- */
p.mermaid {{
    text-align: center;
    margin: 20px 0;
    page-break-inside: avoid;
}}

p.mermaid img {{
    max-width: 95%;
    height: auto;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}}

div.mermaid-error {{
    background: #fff3cd;
    border: 1px dashed #ffc107;
    padding: 12px;
    border-radius: 4px;
    color: #856404;
}}

/* ---------- 章节扉页 ---------- */
.chapter-cover {{
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    page-break-after: always;
}}

.chapter-cover h1 {{
    font-size: 36pt;
    color: #0d1b2a;
    border: none;
    margin: 0;
}}

.chapter-cover .subtitle {{
    font-size: 14pt;
    color: #5fa8d3;
    margin-top: 16px;
}}

/* ---------- 页面 / 分页 ---------- */
section {{ page-break-before: always; }}
section.page-frontmatter {{ page-break-before: avoid; }}

/* ---------- @page 页眉页脚 ---------- */
@page {{
    size: A4;
    margin: 22mm 18mm 22mm 18mm;

    @top-left {{
        content: "《AGENT 七层手册》· 晴暖";
        font-size: 8.5pt;
        color: #888;
        font-family: "Microsoft YaHei", sans-serif;
    }}

    @top-right {{
        content: string(chapter);
        font-size: 8.5pt;
        color: #1b4965;
        font-weight: 600;
        font-family: "Microsoft YaHei", sans-serif;
    }}

    @bottom-left {{
        content: "CC BY-NC-SA 4.0";
        font-size: 8pt;
        color: #aaa;
    }}

    @bottom-center {{
        content: counter(page) " / " counter(pages);
        font-size: 9pt;
        color: #555;
        font-family: "Consolas", monospace;
    }}

    @bottom-right {{
        content: "2026-06-25";
        font-size: 8pt;
        color: #aaa;
    }}
}}

@page :first {{
    @top-left {{ content: ""; }}
    @top-right {{ content: ""; }}
    @bottom-left {{ content: ""; }}
    @bottom-right {{ content: ""; }}
}}

h1 {{ string-set: chapter content(); }}
"""


# ---------- HTML 拼接 ----------

def _build_html(sections_html: str, pygments_css: str) -> str:
    css = CSS_TEMPLATE.format(style=PYMENTS_STYLE, pygments_css=pygments_css, code_font=CODE_FONT)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>《AGENT 七层手册》</title>
<style>
{css}
</style>
</head>
<body>
{sections_html}
</body>
</html>
"""


# ---------- Chrome headless 调用 ----------

CHROME_PATHS = [
    r"C:/Program Files/Google/Chrome/Application/chrome.exe",
    r"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
    r"C:/Program Files/Microsoft/Edge/Application/msedge.exe",
]


def _find_chrome() -> str:
    for p in CHROME_PATHS:
        if Path(p).exists():
            return p
    raise FileNotFoundError("未找到 Chrome / Edge，请安装 Google Chrome")


def _html_to_pdf(html_path: Path, pdf_path: Path):
    chrome = _find_chrome()
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--font-render-hinting=none",
        f"--print-to-pdf={pdf_path.resolve()}",
        "--print-to-pdf-no-header",
        "--virtual-time-budget=10000",
        str(html_path.resolve()),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if result.returncode != 0:
        print("Chrome stderr:", result.stderr[:500], file=sys.stderr)
        raise RuntimeError(f"Chrome 失败 exit={result.returncode}")


# ---------- 主流程 ----------

def main() -> int:
    DIST.mkdir(parents=True, exist_ok=True)
    md = _build_markdown()

    pygments_css = HtmlFormatter(style=PYMENTS_STYLE).get_style_defs(".highlight")

    files = _collect_files()
    print(f"收集到 {len(files)} 个 Markdown 文件")

    sections: list[str] = []
    for md_path, layer, title in files:
        try:
            sec_html = _file_to_html(md, md_path, layer, title)
            sections.append(sec_html)
            print(f"  ✓ {layer}/{md_path.name}")
        except Exception as e:
            print(f"  ✗ {layer}/{md_path.name}: {e}", file=sys.stderr)

    full_html = _build_html("\n".join(sections), pygments_css)
    html_path = DIST / "AGENT七层手册.html"
    html_path.write_text(full_html, encoding="utf-8")
    print(f"\nHTML: {html_path} ({len(full_html) // 1024} KB)")

    pdf_path = DIST / "AGENT七层手册.pdf"
    print(f"\n渲染 PDF via Chrome headless ...")
    _html_to_pdf(html_path, pdf_path)

    size_mb = pdf_path.stat().st_size / 1024 / 1024
    print(f"\n✅ PDF: {pdf_path} ({size_mb:.2f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())