#!/usr/bin/env bash


SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source $SCRIPT_DIR/env.sh

wget https://github.com/githubcatw/DeepFaceLab_Linux/releases/download/xseg/model_generic_xseg.zip
unzip -q model_generic_xseg.zip -d "$DFL_WORKSPACE/model"
rm model_generic_xseg.zip