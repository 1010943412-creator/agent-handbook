#!/usr/bin/env bash
# 一键运行三道验收关：字数 / 引用 / 图表
# 用法：
#   bash scripts/run_all_checks.sh <dir>              # L1-L7 节模式 (800-1500 字, ≥1 图)
#   bash scripts/run_all_checks.sh --mode=case <dir>  # L8 案例模式 (1200-2500 字, ≥2 图)
set -e

# Python 解释器 fallback：python3 -> python -> py
PYTHON=$(command -v python3 || command -v python || command -v py)
if [ -z "$PYTHON" ]; then
    echo "Error: python interpreter not found (looked for python3/python/py)"
    exit 1
fi

# 解析参数
MODE="section"
DIR=""
while [ $# -gt 0 ]; do
    case "$1" in
        --mode=*)
            MODE="${1#--mode=}"
            shift
            ;;
        *)
            DIR="$1"
            shift
            ;;
    esac
done

if [ -z "$DIR" ]; then
    DIR="handbook"
fi
if [ ! -d "$DIR" ]; then
    echo "Error: $DIR not found"
    exit 1
fi

export PYTHONIOENCODING=utf-8

if [ "$MODE" = "case" ]; then
    echo "=== L8 案例模式验收检查开始 ==="
    echo "[1/3] 案例字数检查 (1200-2500)"
    "$PYTHON" scripts/check_case_word_count.py "$DIR"
    echo "[2/3] 引用检查 (≥4 S/A 级,沿用节模式脚本)"
    "$PYTHON" scripts/check_references.py "$DIR"
    echo "[3/3] 案例图表检查 (≥2 张)"
    "$PYTHON" scripts/check_case_figures.py "$DIR"
else
    echo "=== L1-L7 节模式验收检查开始 ==="
    echo "[1/3] 字数检查 (800-1500)"
    "$PYTHON" scripts/check_word_count.py "$DIR"
    echo "[2/3] 引用检查"
    "$PYTHON" scripts/check_references.py "$DIR"
    echo "[3/3] 图表检查 (≥1 张)"
    "$PYTHON" scripts/check_figures.py "$DIR"
fi
echo "=== 全部通过 ==="