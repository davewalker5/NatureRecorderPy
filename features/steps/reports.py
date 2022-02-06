from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from features.steps.helpers import select_option, get_date_from_string, confirm_table_row_count
from naturerec_model.model import Sighting


@when("I navigate to the location report page")
def _(context):
    url = context.flask_runner.make_url("reports/location")
    context.browser.get(url)
    assert "Location Report" in context.browser.title


@when("I fill in the location report details")
def _(context):
    row = context.table.rows[0]
    select_option(context, "location", row["Location"], None)
    select_option(context, "category", row["Category"], None)
    from_date = get_date_from_string(row["From"]).strftime(Sighting.DATE_DISPLAY_FORMAT)
    context.browser.find_element(By.NAME, "from_date").send_keys(from_date)
    context.browser.find_element(By.NAME, "from_date").send_keys(Keys.ENTER)

@then("There will be {number} results in the report table")
@then("There will be {number} result in the report table")
def _(context, number):
    confirm_table_row_count(context, number, 5)
