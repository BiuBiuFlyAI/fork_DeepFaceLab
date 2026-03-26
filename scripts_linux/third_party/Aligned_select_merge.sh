#!/usr/bin/env bash


SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_SCRIPT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
USE_ROOT_SCRIPT_DIR=1

source $ROOT_SCRIPT_DIR/env.sh

$DFL_PYTHON "$DFL_SRC/third_party/facesets/facesets.py"
