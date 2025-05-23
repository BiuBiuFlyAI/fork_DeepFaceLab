#!/usr/bin/env bash


SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source $SCRIPT_DIR/env.sh

$DFL_PYTHON "$DFL_SRC/main.py" xseg fetch \
    --input-dir "$DFL_WORKSPACE/data_dst/aligned"