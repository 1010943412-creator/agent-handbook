"""最小验证: markdown-it + Pygments 高亮 + Chrome headless PDF"""
import asyncio
from pathlib import Path
from markdown_it import MarkdownIt
from pygments import highlight
from pygments.lexers import get_lexer_by_name, PythonLexer
from pygments.formatters import HtmlFormatter
import subprocess

def _highlight(code: str, lang: str) -> str:
    try:
        lexer = get_lexer_by_name(lang)
    except Exception:
        lexer = PythonLexer()
    formatter = HtmlFormatter(style=PYGMENTS_STYLE, cssclass="highlight", nobackground=False)
    return highlight(code, lexer, formatter)


md = MarkdownIt(
    "gfm-like",
    {
        "html": True,
        "typographer": True,
        "highlight": lambda code, lang, attrs: _highlight(code, lang),
    },
)

PYGMENTS_STYLE = "vs"  # 颜色主题: vs / monokai / one-dark / github-dark / friendly


def highlight_code(code: str, lang: str) -> str:
    try:
        lexer = get_lexer_by_name(lang)
    except Exception:
        lexer = PythonLexer()
    formatter = HtmlFormatter(style=PYGMENTS_STYLE, cssclass="highlight", nobackground=False)
    return highlight(code, lexer, formatter)


# 自定义 fence 渲染器应用 Pygments

sample = """# 1.1 LLM 速通：Transformer 推理路径

## 推理路径

Transformer 推理分为 **Prefill** 和 **Decode** 两个阶段：

```mermaid
graph LR
    A[输入 Token 序列] --> B[Prefill<br/>并行计算 KV]
    B --> C[Decode<br/>逐 token 生成]
    C --> D[输出序列]
```

## 代码示例

```python
from transformers import AutoModelForCausalLM
import torch

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-7B",
    torch_dtype=torch.bfloat16,
    device_map="auto"
)
inputs = tokenizer("什么是 AGENT?", return_tensors="pt").to("cuda")
output = model.generate(**inputs, max_new_tokens=100)
print(tokenizer.decode(output[0]))
```

## 关键点

> Prefill 阶段是计算密集型，Decode 阶段是内存密集型。
> 这就是为什么 KV Cache 优化如此重要。

| 阶段 | 计算模式 | 瓶颈 | 优化方向 |
|---|---|---|---|
| Prefill | 并行 GEMM | 算力 | Tensor Parallel |
| Decode | 串行 GEMV | 显存带宽 | KV Cache + FlashAttention |
"""

html_body = md.render(sample)

# 用 Pygments CSS + 自定义样式
pygments_css = HtmlFormatter(style=PYGMENTS_STYLE).get_style_defs(".highlight")

full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>Sample</title>
<style>
{pygments_css}

body {{
    font-family: "Microsoft YaHei", "PingFang SC", "SimSun", sans-serif;
    font-size: 11pt;
    line-height: 1.7;
    color: #1a1a1a;
    max-width: 800px;
    margin: 40px auto;
    padding: 0 40px;
}}

h1 {{ font-size: 26pt; color: #1b4965; border-bottom: 3px solid #1b4965; padding-bottom: 8px; }}
h2 {{ font-size: 17pt; color: #1b4965; margin-top: 30px; }}
h3 {{ font-size: 13pt; color: #5fa8d3; }}

pre.highlight {{
    background: #f8f9fa;
    border-left: 4px solid #5fa8d3;
    border-radius: 4px;
    padding: 12px 16px;
    overflow-x: auto;
    font-size: 9.5pt;
    line-height: 1.5;
    page-break-inside: avoid;
}}

code {{
    font-family: "Consolas", "FangSong", monospace;
}}

blockquote {{
    border-left: 4px solid #5fa8d3;
    margin: 16px 0;
    padding: 8px 16px;
    background: #f0f4f8;
    color: #333;
}}

table {{
    border-collapse: collapse;
    width: 100%;
    margin: 16px 0;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 8px 12px;
    text-align: left;
}}

th {{
    background: #1b4965;
    color: white;
}}

tr:nth-child(even) {{ background: #f8f9fa; }}

@page {{
    size: A4;
    margin: 20mm 18mm 22mm 18mm;
    @top-left {{ content: "AGENT 七层手册 · L1"; font-size: 9pt; color: #888; }}
    @top-right {{ content: "1.1 LLM 速通"; font-size: 9pt; color: #888; }}
    @bottom-center {{ content: counter(page) " / " counter(pages); font-size: 9pt; color: #888; }}
}}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

out_html = Path("build/dist/sample.html")
out_html.write_text(full_html, encoding="utf-8")

# Chrome headless → PDF
chrome = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
cmd = [
    chrome,
    "--headless",
    "--disable-gpu",
    "--no-sandbox",
    f"--print-to-pdf={Path('build/dist/sample.pdf').resolve()}",
    "--print-to-pdf-no-header",
    str(out_html.resolve()),
]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
print("Chrome exit:", result.returncode)
if result.stderr:
    print("stderr:", result.stderr[:300])

print(f"PDF: {Path('build/dist/sample.pdf').stat().st_size} bytes")