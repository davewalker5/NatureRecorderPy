#!/usr/bin/env bash
set -euo pipefail

DOCS_FOLDER="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PROJECT_ROOT="$DOCS_FOLDER/.."
export PYTHONPATH="$PROJECT_ROOT/src"

echo "Documents Folder : $DOCS_FOLDER"
echo "Project Root     : $PROJECT_ROOT"
echo "Python Path      : $PYTHONPATH"

# The assumption is there is already a virtual environment with the requirements to
# run the application installed. This adds the documentation dependencies.
. "$PROJECT_ROOT/venv/bin/activate"
trap deactivate EXIT
python -m pip install "$DOCS_FOLDER"

# Build the documentation
make -C "$DOCS_FOLDER" html
