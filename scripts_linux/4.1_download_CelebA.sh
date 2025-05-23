#!/usr/bin/env bash


SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source $SCRIPT_DIR/env.sh

wget https://github.com/nagadit/DeepFaceLab_Linux/releases/download/1.0/pretrain_CelebA.zip
unzip -q pretrain_CelebA.zip -d "$DFL_WORKSPACE/pretrain/aligned_debug"
rm pretrain_CelebA.zip