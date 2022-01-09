from behave import given, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from naturerec_model.model import Gender
from naturerec_model.logic import create_sighting
from helpers import get_date_from_string, create_test_location, create_test_category, create_test_species


@given("A set of sightings")
def _(context):
    """
    Create one or more sightings presented in a data table in the following form:

    | Date       | Location      | Category | Species   | Number | Gender | WithYoung |
    | 01/01/2022 | Test Location | Birds    | Blackbird | 1      | Male   | No        |

    :param context: Behave context
    """
    for row in context.table:
        sighting_date = get_date_from_string(row["Date"])
        location = create_test_location(row["Location"])
        category = create_test_category(row["Category"])
        species = create_test_species(row["Species"], category.id)
        gender = [key for key, value in Gender.gender_map().items() if value == row["Gender"]][0]
        with_young = 1 if row["WithYoung"] == "Yes" else 0
        _ = create_sighting(location.id, species.id, sighting_date, int(row["Number"]), gender, with_young)


@when("I select \"{selection}\" as the \"{selector}\"")
def _(context, selection, selector):
    """
    Select list selector

    :param context: Behave context
    :param selection: Visible text for the selection
    :param selector: Name of the select list element
    """
    selector = Select(context.browser.find_element(By.NAME, selector))
    selector.select_by_visible_text(selection)


@when("I click on the \"{button_text}\" button")
def _(context, button_text):
    """
    Button clicker based on the button text

    :param context: Behave context
    :param button_text: Button text
    """
    xpath = f"//button[text()='{button_text}']"
    button = context.browser.find_element(By.XPATH, xpath)
    button.click()
