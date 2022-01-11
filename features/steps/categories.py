import time
from behave import given,  when, then
from selenium.webdriver.common.by import By
from helpers import confirm_table_row_count, confirm_span_exists


@given("I navigate to the category list page")
@when("I navigate to the category list page")
def _(context):
    url = context.flask_runner.make_url("categories/list")
    context.browser.get(url)
    assert "Categories" in context.browser.title


@when("I fill in the category details")
def _(context):
    # Having clicked, we need to sleep this thread to allow the server round trip to  refresh the page.
    # WebDriverWait won't work in this context
    time.sleep(1)
    row = context.table.rows[0]
    context.browser.find_element(By.NAME, "name").send_keys(row["Category"])


@then("There will be {number} categories in the category list")
@then("There will be {number} category in the category list")
def _(context, number):
    confirm_table_row_count(context, number, 1)


@then("The category list will be empty")
def _(context):
    confirm_span_exists(context, "There are no categories in the database", 1)
