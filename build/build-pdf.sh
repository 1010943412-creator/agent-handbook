#!/usr/bin/env bash
# 构建 AGENT 七层手册 PDF
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p build/dist
shopt -s nullglob

# 字体检测：Source Han Sans SC 不可用时回退到 Noto Sans CJK SC
MAIN_FONT="Source Han Sans SC"
if command -v fc-list > /dev/null 2>&1; then
    if ! fc-list | grep -q "Source Han Sans SC"; then
        echo "Warning: Source Han Sans SC not found, falling back to Noto Sans CJK SC"
        MAIN_FONT="Noto Sans CJK SC"
    fi
fi

PANDOC_INPUTS=("README.md")
LAYERS=(l1-theory l2-context l3-protocol l4-framework l5-pattern l6-observability l7-production l8-cases)
for layer in "${LAYERS[@]}"; do
    if [ -d "handbook/$layer" ]; then
        for md in handbook/$layer/*.md; do
            PANDOC_INPUTS+=("$md")
        done
    else
        echo "Skip: handbook/$layer not found"
    fi
done
if compgen -G "appendix/*.md" > /dev/null; then
    for md in appendix/*.md; do
        PANDOC_INPUTS+=("$md")
    done
else
    echo "Skip: appendix/*.md not found"
fi

pandoc "${PANDOC_INPUTS[@]}" -o build/dist/AGENT七层手册.pdf \
  --pdf-engine=xelatex \
  -V "mainfont=$MAIN_FONT" \
  -V "monofont=JetBrains Mono" \
  -V geometry:margin=2.5cm \
  --toc --toc-depth=2 \
  --highlight-style=tango

echo "PDF 已生成: build/dist/AGENT七层手册.pdf"
