#!/usr/bin/env bash


SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source $SCRIPT_DIR/env.sh

$DFL_PYTHON "$DFL_SRC/main.py" xseg apply \
    --input-dir "$DFL_WORKSPACE/data_src/aligned" \
    --model-dir "$DFL_SRC/model_generic_xseg"
