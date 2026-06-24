#!/usr/bin/env python3
"""将 Markdown 中的 mermaid 代码块渲染为 PNG 图片。

使用 mermaid.ink API (https://mermaid.ink) 在线渲染，
无需安装 mmdc / puppeteer 等重量级依赖。
"""
import base64
import hashlib
import re
import sys
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

MERMAID_RE = re.compile(r'```mermaid\n(.*?)```', re.DOTALL)
CACHE_DIR = Path("build/.mermaid_cache")


def render_mermaid_to_png(mermaid_code: str, output_path: Path) -> Path:
    """渲染单个 mermaid 代码为 PNG。"""
    encoded = base64.urlsafe_b64encode(mermaid_code.encode("utf-8")).decode("ascii")
    url = f"https://mermaid.ink/img/{encoded}"

    cache_key = hashlib.md5(mermaid_code.encode()).hexdigest()
    cache_file = CACHE_DIR / f"{cache_key}.png"
    if cache_file.exists():
        output_path.write_bytes(cache_file.read_bytes())
        return output_path

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    try:
        req = Request(url, headers={"User-Agent": "agent-handbook-builder/1.0"})
        with urlopen(req, timeout=30) as resp:
            data = resp.read()
        cache_file.write_bytes(data)
        output_path.write_bytes(data)
    except URLError as e:
        print(f"WARNING: mermaid.ink 渲染失败: {e}", file=sys.stderr)
        _write_placeholder(output_path, mermaid_code)
    return output_path


def _write_placeholder(path: Path, code: str):
    """mermaid 渲染失败时生成占位图。"""
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGB", (800, 400), "#1a1a2e")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 16)
    except Exception:
        font = ImageFont.load_default()
    lines = code.strip().split("\n")[:12]
    for i, line in enumerate(lines):
        draw.text((20, 20 + i * 24), line, fill="#e0e0e0", font=font)
    draw.text((20, 380), "[mermaid 图 - 需在线渲染]", fill="#888888", font=font)
    img.save(path)


def replace_mermaid_blocks(md_content: str, img_dir: Path) -> str:
    """将 Markdown 中的 ```mermaid...``` 替换为 ![](img_dir/xxx.png)。"""
    img_dir.mkdir(parents=True, exist_ok=True)

    def _replace(match):
        code = match.group(1).strip()
        idx = hashlib.md5(code.encode()).hexdigest()[:8]
        img_path = img_dir / f"mermaid_{idx}.png"
        render_mermaid_to_png(code, img_path)
        return f"![mermaid 图](build/.mermaid_img/mermaid_{idx}.png)"

    return MERMAID_RE.sub(_replace, md_content)


if __name__ == "__main__":
    test_code = "graph TD\n    A[Start] --> B[End]"
    out = Path("build/.mermaid_cache/test.png")
    render_mermaid_to_png(test_code, out)
    print(f"Test image saved to {out}")
