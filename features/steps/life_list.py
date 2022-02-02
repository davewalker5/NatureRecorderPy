from behave import when, then
from selenium.webdriver.common.by import By
from helpers import confirm_table_row_count, confirm_span_exists, get_export_filepath, delete_export_file, select_option


@when("I navigate to the life list page")
def _(context):
    url = context.flask_runner.make_url("life_list/list")
    context.browser.get(url)
    assert "Life List" in context.browser.title


@when("I navigate to the export life list page")
def _(context):
    url = context.flask_runner.make_url("export/life_list")
    context.browser.get(url)
    assert "Export Life List" in context.browser.title


@when("I enter the life list export properties")
def _(context):
    row = context.table.rows[0]
    # We're about to do an export, so if the file already exists then delete it at this stage
    context.export_filepath = get_export_filepath(row["Filename"])
    delete_export_file(row["Filename"])

    context.browser.find_element(By.NAME, "filename").send_keys(row["Filename"])
    select_option(context, "category", row["Category"], 0)


@then("There will be {number} species in the life list")
@then("There will be {number} species in the life list")
def _(context, number):
    confirm_table_row_count(context, number, 1)


@then("The life list will be empty")
def _(context):
    confirm_span_exists(context, "There are no species in the database for the specified category", 1)


@then("The life list export starts")
def _(context):
    confirm_span_exists(context, "The selected life list is exporting in the background", 1)
