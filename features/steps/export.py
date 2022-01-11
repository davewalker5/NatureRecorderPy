import time
from behave import when, then
from selenium.webdriver.common.by import By
from helpers import select_option, confirm_span_exists, get_export_filepath, delete_export_file


@when("I navigate to the export page")
def _(context):
    url = context.flask_runner.make_url("export/filters")
    context.browser.get(url)
    assert "Export Sightings" in context.browser.title


@when("I enter the export properties")
def _(context):
    row = context.table.rows[0]
    # We're about to do an export, so if the file already exists then delete it at this stage
    context.export_filepath = get_export_filepath(row["Filename"])
    delete_export_file(row["Filename"])

    context.browser.find_element(By.NAME, "filename").send_keys(row["Filename"])
    if row["Location"].strip():
        select_option(context, "location", row["Location"], 0)

    if row["Category"].strip():
        select_option(context, "category", row["Category"], 0)

    if row["Species"].strip():
        select_option(context, "species", row["Species"], 1)


@then("The export starts")
def _(context):
    confirm_span_exists(context, "Matching sightings are exporting in the background", 1)


@then("There will be {number} sightings in the export file")
@then("There will be {number} sighting in the export file")
def _(context, number):
    time.sleep(2)
    with open(context.export_filepath, mode="rt", encoding="utf-8") as f:
        lines = f.readlines()
    # Number of lines plus 1 to account for the headers
    assert len(lines) == int(number) + 1
