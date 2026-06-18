#!/usr/bin/env bash
set -e
echo "=== 验收检查开始 ==="
DIR="${1:-handbook}"
echo "[1/3] 字数检查"
python3 scripts/check_word_count.py "$DIR" || true
echo "[2/3] 引用检查"
python3 scripts/check_references.py "$DIR" || true
echo "[3/3] 图表检查"
python3 scripts/check_figures.py "$DIR" || true
echo "=== 检查完成 ==="
