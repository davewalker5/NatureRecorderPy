@ECHO OFF
SET PROJECT_ROOT=%~p0
CALL %PROJECT_ROOT%\venv\Scripts\activate.bat
SET PYTHONPATH=%PROJECT_ROOT%src
SET NATURE_RECORDER_DB=%PROJECT_ROOT%data\naturerecorder.db
SET FLASK_ENV=development

ECHO Project root      = %PROJECT_ROOT%
ECHO Python Path       = %PYTHONPATH%
ECHO Database Path     = %NATURE_RECORDER_DB%
ECHO Flask Environment = %FLASK_ENV%

python -m naturerec_web
ECHO ON
