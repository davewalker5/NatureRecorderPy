#!/bin/bash -f

REPORTS_ROOT=$( cd "$( dirname "$0" )" && pwd )
cd "$REPORTS_ROOT"
. $REPORTS_ROOT/venv/bin/activate

pip freeze --local | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip3 install -U 
pip install -e .
