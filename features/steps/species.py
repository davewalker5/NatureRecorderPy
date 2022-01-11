import time
from behave import when, then
from selenium.webdriver.common.by import By
from helpers import confirm_table_row_count, confirm_span_exists, select_option


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
    select_option(context, "category", row["Category"], 0)
    context.browser.find_element(By.NAME, "name").send_keys(row["Species"])


@then("There will be {number} species in the species list")
@then("There will be {number} species in the species list")
def _(context, number):
    confirm_table_row_count(context, number, 1)


@then("The species list will be empty")
def _(context):
    confirm_span_exists(context, "There are no species in the database for the specified category", 1)
