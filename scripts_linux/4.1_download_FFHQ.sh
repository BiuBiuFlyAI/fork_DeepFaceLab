#!/usr/bin/env bash


SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source $SCRIPT_DIR/env.sh

wget https://github.com/nagadit/DeepFaceLab_Linux/releases/download/1.0/pretrain_FFHQ.zip
unzip -q pretrain_FFHQ.zip -d "$DFL_WORKSPACE/pretrain/aligned_debug"
rm pretrain_FFHQ.zip