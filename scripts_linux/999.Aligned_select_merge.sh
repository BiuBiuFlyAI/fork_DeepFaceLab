#!/usr/bin/env bash


SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source $SCRIPT_DIR/env.sh

export PYTHONPATH=$DFL_SRC:$PYTHONPATH

$DFL_PYTHON "$DFL_SRC/facesets/facesets.py"
