import time
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


@when("I navigate to the species list page")
def _(context):
    url = context.flask_runner.make_url("species/list")
    context.browser.get(url)
    time.sleep(1)
    assert "Species" in context.browser.title


@when("I fill in the species details")
def _(context):
    # Having clicked, we need to sleep this thread to allow the server round trip to  refresh the page.
    # WebDriverWait won't work in this context
    time.sleep(1)
    row = context.table.rows[0]
    selector = Select(context.browser.find_element(By.NAME, "category"))
    selector.select_by_visible_text(row["Category"])
    context.browser.find_element(By.NAME, "name").send_keys(row["Species"])


@then("There will be {number} species in the species list")
@then("There will be {number} species in the species list")
def _(context, number):
    # Having clicked, we need to sleep this thread to allow the server round trip to pull the results and
    # refresh the page. WebDriverWait won't work in this context
    time.sleep(1)
    table = context.browser.find_element(By.CLASS_NAME, "striped")
    table_body = table.find_element(By.XPATH, ".//tbody")
    table_rows = table_body.find_elements(By.XPATH, ".//tr")
    expected = int(number)
    actual = len(table_rows)
    assert actual == expected


@then("The species list will be empty")
def _(context):
    # Having clicked, we need to sleep this thread to allow the server round trip to pull the results and
    # refresh the page. WebDriverWait won't work in this context
    time.sleep(1)
    xpath = f"//span"  # [text()='There are no species in the database for the specified category']"
    _ = context.browser.find_element(By.XPATH, xpath)
