@ECHO OFF
SET PROJECT_ROOT=%~p0
CALL %PROJECT_ROOT%\venv\Scripts\activate.bat
SET PYTHONPATH=%PROJECT_ROOT%src;%PROJECT_ROOT%tests

ECHO Project root      = %PROJECT_ROOT%
ECHO Python Path       = %PYTHONPATH%

CD tests\locust_tests
locust -f locustfile.py
ECHO ON
