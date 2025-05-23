#!/usr/bin/env bash


SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source $SCRIPT_DIR/env.sh

wget https://github.com/nagadit/DeepFaceLab_Linux/releases/download/1.0/pretrain_Quick96.zip
unzip -q pretrain_Quick96.zip -d "$DFL_WORKSPACE/pretrain/pretrain_Quick96"
rm pretrain_Quick96.zip