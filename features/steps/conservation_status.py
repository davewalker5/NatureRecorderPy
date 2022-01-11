import time
from behave import given,  when, then
from selenium.webdriver.common.by import By
from helpers import confirm_table_row_count


@given("I navigate to the conservation status schemes page")
@when("I navigate to the conservation status schemes page")
def _(context):
    url = context.flask_runner.make_url("status/list")
    context.browser.get(url)
    assert "Conservation Status Schemes" in context.browser.title


@when("I enter the conservation status scheme name")
def _(context):
    # This action's preceded by clicking on a button, so give the page a moment to serve
    time.sleep(1)
    row = context.table.rows[0]
    context.browser.find_element(By.NAME, "name").send_keys(row["Scheme"])


@when("I enter the conservation status rating name")
def _(context):
    # This action's preceded by clicking on a button, so give the page a moment to serve
    time.sleep(1)
    row = context.table.rows[0]
    context.browser.find_element(By.NAME, "name").send_keys(row["Rating"])


@then("There will be {number} schemes in the schemes list")
@then("There will be {number} scheme in the schemes list")
@then("There will be {number} ratings in the ratings list")
@then("There will be {number} rating in the ratings list")
def _(context, number):
    confirm_table_row_count(context, number, 1)
