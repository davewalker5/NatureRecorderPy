#!/bin/zsh -f

export PROJECT_ROOT=$( cd "$(dirname "$0")" ; pwd -P )
source "$PROJECT_ROOT/venv/bin/activate"
export PYTHONPATH="$PROJECT_ROOT/src"
export FLIGHT_BOOKING_DB="$PROJECT_ROOT/data/naturerecorder.db"
export FLASK_ENV=development
export FLASK_APP=naturerecorder.py
cd src/naturerec_web && flask run
