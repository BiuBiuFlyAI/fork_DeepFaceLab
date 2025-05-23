#!/usr/bin/env bash


conda activate deepfacelab

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

export DFL_ROOT="$(realpath "$SCRIPT_DIR/../..")"
export DFL_SRC="$DFL_ROOT/DeepFaceLab"
export DFL_WORKSPACE="$DFL_ROOT/workspace"
export DFL_PYTHON="python3"

if [ ! -d "$DFL_WORKSPACE" ]; then
    mkdir -p "$DFL_WORKSPACE"
    mkdir -p "$DFL_WORKSPACE/data_src"
    mkdir -p "$DFL_WORKSPACE/data_src/aligned"
    mkdir -p "$DFL_WORKSPACE/data_src/aligned_debug"
    mkdir -p "$DFL_WORKSPACE/data_dst"
    mkdir -p "$DFL_WORKSPACE/data_dst/aligned"
    mkdir -p "$DFL_WORKSPACE/data_dst/aligned_debug"
    mkdir -p "$DFL_WORKSPACE/pretrain"
    mkdir -p "$DFL_WORKSPACE/pretrain/aligned"
    mkdir -p "$DFL_WORKSPACE/pretrain/aligned_debug"
    mkdir -p "$DFL_WORKSPACE/pretrain/pretrain_Quick96"
    mkdir -p "$DFL_WORKSPACE/model"
fi
