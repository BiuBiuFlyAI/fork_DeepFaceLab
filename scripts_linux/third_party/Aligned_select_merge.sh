#!/usr/bin/env bash


SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PARENT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

source PARENT_DIR/env.sh

export PYTHONPATH=$DFL_SRC:$PYTHONPATH

$DFL_PYTHON "$DFL_SRC/third_party/facesets/facesets.py"
