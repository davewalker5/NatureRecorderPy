#!/bin/sh -f

export PROJECT_ROOT=$( cd "$( dirname "$0" )" && pwd )
. $PROJECT_ROOT/venv/bin/activate
export PYTHONPATH=$PROJECT_ROOT/src

echo "Project root      = $PROJECT_ROOT"
echo "Python Path       = $PYTHONPATH"

python -m unittest
