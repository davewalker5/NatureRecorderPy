import datetime
from behave import given, when, then
from helpers import confirm_table_row_count, create_test_location, create_test_category, create_test_species
from src.naturerec_model.model import Gender, Session, JobStatus
from src.naturerec_model.logic import create_sighting
from src.naturerec_model.data_exchange import SightingsExportHelper

@given("The jobs list is empty")
def _(context):
    with Session.begin() as session:
        jobs = session.query(JobStatus).all()
        for job in jobs:
            session.delete(job)


@given("I have started a sightings export")
def _(context):
    # Create a sighting to export
    sighting_date = datetime.datetime.today().date()
    location = create_test_location("Farmoor Reservoir")
    category = create_test_category("Birds")
    species = create_test_species("Cormorant", category.id)
    gender = [key for key, value in Gender.gender_map().items() if value == "Unknown"][0]
    _ = create_sighting(location.id, species.id, sighting_date, None, gender, 0, None)

    # Kick off the export
    exporter = SightingsExportHelper("sightings.csv", None, None, None, None)
    exporter.start()
    exporter.join()


@when("I navigate to the job list page")
def _(context):
    url = context.flask_runner.make_url("jobs/list")
    context.browser.get(url)
    assert "Background Job Status" in context.browser.title


@then("There will be {number} jobs in the jobs list")
@then("There will be {number} job in the jobs list")
def _(context, number):
    confirm_table_row_count(context, number, 1)
