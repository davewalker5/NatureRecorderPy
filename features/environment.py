import os
import time
import platform
from sqlalchemy import text
from naturerec_model.model import create_database
from naturerec_model.logic import create_user
from behave import fixture, use_fixture
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from flask_app_runner import FlaskAppRunner
from naturerec_web import create_app
from naturerec_model.model.database import Engine
from naturerec_model.model.utils import get_project_path


MAXIMUM_PAGE_LOAD_TIME = 5


@fixture
def start_flask_server(context):
    """
    Start the Nature Recorder web application on a background thread

    :param context:
    """
    context.flask_runner = FlaskAppRunner("127.0.0.1", 5000, create_app("development"))
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
    # Determine the OS and create an appropriate browser instance
    os_name = platform.system()
    if os_name == "Darwin":
        context.browser = webdriver.Safari()
    elif os_name == "Windows":
        # This requires the msedge-selenium-tools package
        context.browser = webdriver.Edge(r"msedgedriver.exe")
    else:
        raise NotImplementedError()

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
    create_user("behave", "password")


@fixture
def login(context):
    """
    Log in to the application

    :param context: Behave context
    """
    # Browse to the login page and enter the username and password
    url = context.flask_runner.make_url("auth/login")
    context.browser.get(url)
    context.browser.find_element(By.NAME, "username").send_keys("behave")
    context.browser.find_element(By.NAME, "password").send_keys("password")

    # Click the "login" button
    xpath = f"//*[text()='Login']"
    elements = context.browser.find_elements(By.XPATH, xpath)
    for element in elements:
        try:
            element.click()
        except (ElementNotInteractableException, NoSuchElementException):
            pass

    time.sleep(1)


def before_all(context):
    """
    Set up the test environment before any scenarios are run

    :param context: Behave context
    """
    use_fixture(create_test_database, context)
    use_fixture(start_flask_server, context)
    use_fixture(start_selenium_browser, context)
    use_fixture(login, context)


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
