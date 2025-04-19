#!/bin/sh -f

export PROJECT_ROOT=$( cd "$( dirname "$0" )" && pwd )
. $PROJECT_ROOT/venv/bin/activate
export PYTHONPATH=$PROJECT_ROOT/src
export NATURE_RECORDER_DB="$PROJECT_ROOT/data/naturerecorder_test.db"

echo "Project root      = $PROJECT_ROOT"
echo "Python Path       = $PYTHONPATH"
echo "Database Path     = $NATURE_RECORDER_DB"

python -m unittest
