#!/bin/zsh -f

export PROJECT_ROOT=$( cd "$(dirname "$0")" ; pwd -P )
source "$PROJECT_ROOT/venv/bin/activate"
export PYTHONPATH="$PROJECT_ROOT/src"
export NATURE_RECORDER_DB="$PROJECT_ROOT/data/naturerecorder.db"
export FLASK_ENV=development
python -m naturerec_web
