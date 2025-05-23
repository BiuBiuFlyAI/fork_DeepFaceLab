#!/usr/bin/env bash


SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source $SCRIPT_DIR/env.sh

$DFL_PYTHON "$DFL_SRC/main.py" train \
    --training-data-src-dir "$DFL_WORKSPACE/data_src/aligned" \
    --training-data-dst-dir "$DFL_WORKSPACE/data_dst/aligned" \
    --pretraining-data-dir "$DFL_WORKSPACE/pretrain/aligned" \
    --pretrained-model-dir "$DFL_WORKSPACE/pretrain/pretrain_Quick96" \
    --model-dir "$DFL_WORKSPACE/model" \
    --model Quick96

