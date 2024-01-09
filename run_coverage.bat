@ECHO OFF
SET PROJECT_ROOT=%~p0
CALL %PROJECT_ROOT%\venv\Scripts\activate.bat
SET PYTHONPATH=%PROJECT_ROOT%src
SET NATURE_RECORDER_DB=%PROJECT_ROOT%\data\naturerecorder_test.db

ECHO Project root      = %PROJECT_ROOT%
ECHO Python Path       = %PYTHONPATH%

coverage run --branch --source src -m unittest discover
coverage html -d cov_html
ECHO ON