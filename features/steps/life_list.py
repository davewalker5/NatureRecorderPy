from behave import when, then
from helpers import confirm_table_row_count, confirm_span_exists


@when("I navigate to the life list page")
def _(context):
    url = context.flask_runner.make_url("life_list/list")
    context.browser.get(url)
    assert "Life List" in context.browser.title


@then("There will be {number} species in the life list")
@then("There will be {number} species in the life list")
def _(context, number):
    confirm_table_row_count(context, number, 1)


@then("The life list will be empty")
def _(context):
    confirm_span_exists(context, "There are no species in the database for the specified category", 1)
