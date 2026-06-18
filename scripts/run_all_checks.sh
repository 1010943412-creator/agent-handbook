#!/usr/bin/env bash
# 一键运行三道验收关：字数 / 引用 / 图表
set -e

# Python 解释器 fallback：python3 -> python -> py
PYTHON=$(command -v python3 || command -v python || command -v py)
if [ -z "$PYTHON" ]; then
    echo "Error: python interpreter not found (looked for python3/python/py)"
    exit 1
fi

echo "=== 验收检查开始 ==="
DIR="${1:-handbook}"
if [ ! -d "$DIR" ]; then
    echo "Error: $DIR not found"
    exit 1
fi

export PYTHONIOENCODING=utf-8
echo "[1/3] 字数检查"
"$PYTHON" scripts/check_word_count.py "$DIR"

echo "[2/3] 引用检查"
"$PYTHON" scripts/check_references.py "$DIR"

echo "[3/3] 图表检查"
"$PYTHON" scripts/check_figures.py "$DIR"

echo "=== 全部通过 ==="
