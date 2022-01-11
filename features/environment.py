import os
from sqlalchemy import text
from naturerec_model.model import create_database
from behave import fixture, use_fixture
from selenium import webdriver
from flask_app_runner import FlaskAppRunner
from naturerec_web import app as nature_recorder_app
from naturerec_model.model.database import Engine
from naturerec_model.model.utils import get_project_path


MAXIMUM_PAGE_LOAD_TIME = 5


@fixture
def start_flask_server(context):
    """
    Start the Nature Recorder web application on a background thread

    :param context:
    """
    context.flask_runner = FlaskAppRunner("127.0.0.1", 5000, nature_recorder_app)
    context.flask_runner.start()
    yield context.flask_runner

    # As this behaves like a context manager, the following is called after the after_all() hook
    context.flask_runner.stop_server()
    context.flask_runner.join()


@fixture
def start_selenium_browser(context):
    """
    Start a web browser to run the behave tests

    :param context: Behave context
    """
    # TODO: Cross-platform default browser
    context.browser = webdriver.Safari()
    context.browser.implicitly_wait(MAXIMUM_PAGE_LOAD_TIME)
    yield context.browser

    # As this behaves like a context manager, the following is called after the after_all() hook
    context.browser.close()


@fixture
def create_test_database(_):
    """
    Create and populate the test database

    :param _: Behave context (not used)
    """
    create_database()


def before_all(context):
    """
    Set up the test environment before any scenarios are run

    :param context: Behave context
    """
    use_fixture(create_test_database, context)
    use_fixture(start_flask_server, context)
    use_fixture(start_selenium_browser, context)


def before_scenario(context, scenario):
    """
    Initialise the database for every scenario

    :param context: Behave context (not used)
    :param scenario: Behave scenario
    """
    clear_down_script = os.path.join(get_project_path(), "features", "sql", "clear_database.sql")
    with open(clear_down_script, mode="rt", encoding="utf-8") as f:
        for statement in f.readlines():
            if statement:
                Engine.execute(text(statement))


def after_all(_):
    """
    Tear down the test environment after all scenarios have run

    :param _: Behave context (not used)
    """
    pass
