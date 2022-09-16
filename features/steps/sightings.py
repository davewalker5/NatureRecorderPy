import datetime
from behave import when, then
from selenium.webdriver.common.by import By
from helpers import confirm_table_row_count, confirm_span_exists, select_option
from src.naturerec_model.model import Sighting


@when("I navigate to the sightings page")
def _(context):
    url = context.flask_runner.make_url("sightings/list")
    context.browser.get(url)
    assert "Sightings" in context.browser.title


@when("I fill in the sightings filter form")
def _(context):
    row = context.table.rows[0]
    select_option(context, "location", row["Location"], None)
    select_option(context, "category", row["Category"], None)
    select_option(context, "species", row["Species"], 1)


@when("I navigate to the sightings entry page")
def _(context):
    url = context.flask_runner.make_url("/sightings/edit")
    context.browser.get(url)
    assert "Add Sighting" in context.browser.title


@when("I fill in the sighting details")
def _(context):
    # Capture the sighting details for use in the confirmation step
    row = context.table.rows[0]
    context.sighting_species = row["Species"]
    context.sighting_location = row["Location"]
    context.sighting_date = datetime.datetime.today().date().strftime(Sighting.DATE_DISPLAY_FORMAT)

    # Select the values
    category = row["Category"]
    select_option(context, "location", row["Location"], None)
    select_option(context, "category", category, None)
    select_option(context, "species", row["Species"], 1)

    # Some controls are only displayed for certain categories
    if category.casefold() in ["birds", "mammals"]:
        context.browser.find_element(By.NAME, "number").send_keys(row["Number"])
        select_option(context, "gender", row["Gender"], 1)
        context.browser.find_element(By.NAME, "with_young").send_keys("")
        select_option(context, "with_young", row["WithYoung"], 1)


@then("There will be {number} sightings in the sightings list")
@then("There will be {number} sighting in the sightings list")
def _(context, number):
    confirm_table_row_count(context, number, 1)


@then("The sightings list will be empty")
def _(context):
    confirm_span_exists(context, "There are no sightings in the database matching the specified criteria", 1)


@then("The sighting will be added to the database")
def _(context):
    text = f"Added sighting of {context.sighting_species} at {context.sighting_location} on {context.sighting_date}"
    confirm_span_exists(context, text, 1)
