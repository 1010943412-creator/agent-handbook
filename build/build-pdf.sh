#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
mkdir -p build/dist
pandoc README.md \
  handbook/l1-theory/*.md \
  handbook/l2-context/*.md \
  handbook/l3-protocol/*.md \
  handbook/l4-framework/*.md \
  handbook/l5-pattern/*.md \
  handbook/l6-observability/*.md \
  handbook/l7-production/*.md \
  handbook/l8-cases/*.md \
  appendix/*.md \
  -o build/dist/AGENT七层手册.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Source Han Sans SC" \
  -V monofont="JetBrains Mono" \
  -V geometry:margin=2.5cm \
  --toc --toc-depth=2 \
  --highlight-style=tango
echo "PDF 已生成: build/dist/AGENT七层手册.pdf"
