#!/usr/bin/env bash


SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source $SCRIPT_DIR/env.sh

export CUDA_HOME_10=/DATA/sdk/cuda/cuda-10.2.89_440.33.01
export CUDNN_HOME_10=/DATA/sdk/cudnn/cudnn-7.6.5.32_cuda10.2

export CUDA_HOME_11=/DATA/sdk/cuda/cuda-11.8.0_520.61.05
export CUDNN_HOME_11=/DATA/sdk/cudnn/cudnn-8.9.7.29_cuda11

export LD_CU_10=$CUDA_HOME_10/lib64:$CUDNN_HOME_10/lib64
export LD_CU_11=$CUDA_HOME_11/lib64:$CUDNN_HOME_11/lib

export LD_LIBRARY_PATH=$LD_CU_10:$LD_CU_11:$LD_LIBRARY_PATH

python $SCRIPT_DIR/test_gpu.py
