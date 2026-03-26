#!/usr/bin/env bash


SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -n "${USE_ROOT_SCRIPT_DIR}" ]; then
  SCRIPT_DIR="$ROOT_SCRIPT_DIR"
fi

########################################################################################################################

export DFL_ROOT="$(realpath "$SCRIPT_DIR/..")"
export DFL_SRC="$DFL_ROOT/src"
export DFL_WORKSPACE="$DFL_ROOT/workspace"
export DFL_PYTHON="python3"

export PYTHONPATH=$DFL_SRC

########################################################################################################################

export CUDA_HOME_10=/DATA/sdk/cuda/cuda-10.2.89_440.33.01
export CUDNN_HOME_10=/DATA/sdk/cudnn/cudnn-7.6.5.32_cuda10.2

export CUDA_HOME_11=/DATA/sdk/cuda/cuda-11.8.0_520.61.05
export CUDNN_HOME_11=/DATA/sdk/cudnn/cudnn-8.9.7.29_cuda11

export LD_CU_10=$CUDA_HOME_10/lib64:$CUDNN_HOME_10/lib64
export LD_CU_11=$CUDA_HOME_11/lib64:$CUDNN_HOME_11/lib

export LD_LIBRARY_PATH=$LD_CU_10:$LD_CU_11

########################################################################################################################

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
