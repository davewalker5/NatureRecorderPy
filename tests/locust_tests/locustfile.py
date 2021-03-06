import os
import time
import datetime
from bs4 import BeautifulSoup
from random import randrange
from locust import HttpUser, task, between, events
from locust_tests.flask_app_runner import FlaskAppRunner
from naturerec_model.model import create_database, get_data_path, Sighting
from naturerec_model.logic import list_locations, list_categories, list_species, create_user
from naturerec_model.data_exchange import SightingsImportHelper, StatusImportHelper
from naturerec_web import create_app

TEST_USER_NAME = "locust"
TEST_PASSWORD = "password"


flask_runner = FlaskAppRunner("127.0.0.1", 5000, create_app())


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """
    Before any tests run, start the Flask application

    :param environment: Ignored
    :param kwargs: Ignored
    """
    # Reset the database
    create_database()

    # Create a login
    create_user(TEST_USER_NAME, TEST_PASSWORD)

    # Import some sample sightings
    sightings_file = os.path.join(get_data_path(), "imports", "locust_sightings.csv")
    with open(sightings_file, mode="rt", encoding="utf-8") as f:
        importer = SightingsImportHelper(f)
        importer.start()
        importer.join()

    # Import a sample conservation status scheme
    scheme_file = os.path.join(get_data_path(), "imports", "locust_bocc5.csv")
    with open(scheme_file, mode="rt", encoding="utf-8") as f:
        importer = StatusImportHelper(f)
        importer.start()
        importer.join()

    # Start the site
    global flask_runner
    flask_runner.start()


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """
    When the tests complete, stop the Flask application

    :param environment: Ignored
    :param kwargs: Ignored
    """
    global flask_runner
    flask_runner.stop_server()
    flask_runner.join()


class NatureRecorderUser(HttpUser):
    """
    Locust load test, targeting the Nature Recorder application hosted locally in the flask development server. The
    tests are weighted as follows:

    +----------------------------------+----+
    | Test                             | %  |
    +----------------------------------+----+
    | go_to_home_page                  | 1  |
    +----------------------------------+----+
    | list_locations                   | 1  |
    +----------------------------------+----+
    | add_location                     | 1  |
    +----------------------------------+----+
    | list_categories                  | 1  |
    +----------------------------------+----+
    | add_category                     | 1  |
    +----------------------------------+----+
    | list_species                     | 1  |
    +----------------------------------+----+
    | add_species                      | 1  |
    +----------------------------------+----+
    | list_sightings                   | 20 |
    +----------------------------------+----+
    | add_sighting                     | 70 |
    +----------------------------------+----+
    | list_conservation_status_schemes | 1  |
    +----------------------------------+----+
    | show_life_list                   | 1  |
    +----------------------------------+----+
    | list_recent_background_jobs      | 1  |
    +----------------------------------+----+
    """

    #: Simulated users will wait between 1 and 5 seconds per task
    wait_time = between(1, 5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._locations = None
        self._categories = None

    def on_start(self):
        """
        Establish some facts about the data so the tests can simulate realistic actions
        """
        self._locations = list_locations()
        self._categories = list_categories()
        self._login()

    @task
    def go_to_home_page(self):
        """
        Task to open the home page of the application
        """
        self.client.get("/")

    @task
    def list_locations(self):
        """
        Task to simulate listing the locations
        """
        self.client.get("/locations/list")

    @task
    def add_location(self):
        """
        Task to simulate adding a location
        """
        csrf_token = self._get_csrf_token_for_form("/locations/edit")
        name = self._get_name("Location")
        county = self._get_name("County")
        country = self._get_name("Country")
        self.client.post("/locations/edit", data={
            "name": name,
            "address": "",
            "city": "",
            "county": county,
            "postcode": "",
            "country": country,
            "latitude": "",
            "longitude": "",
            "csrf_token": csrf_token
        })

    @task
    def list_categories(self):
        """
        Task to simulate listing the categories
        """
        self.client.get("/categories/list")

    @task
    def add_category(self):
        """
        Task to simulate adding a category
        """
        csrf_token = self._get_csrf_token_for_form("/categories/edit")
        name = self._get_name("Category")
        self.client.post("/categories/edit", data={
            "name": name,
            "csrf_token": csrf_token
        })

    @task
    def list_species(self):
        """
        Task to simulate listing the species belonging to a selected category
        """
        csrf_token = self._get_csrf_token_for_form("/species/list")
        category_id = self._get_random_category_id()
        self.client.post("/species/list", data={
            "category": str(category_id),
            "csrf_token": csrf_token
        })

    @task
    def add_species(self):
        """
        Task to simulate adding a species
        """
        csrf_token = self._get_csrf_token_for_form("/species/add")
        category_id = self._get_random_category_id()
        name = self._get_name("Species")
        self.client.post("/species/add", data={
            "category": str(category_id),
            "name": name,
            "csrf_token": csrf_token
        })

    @task(20)
    def list_sightings(self):
        """
        Task to simulate listing the sightings
        """
        self.client.get("/sightings/list")

    @task(70)
    def add_sighting(self):
        """
        Task to simulate adding a new sighting
        """
        csrf_token = self._get_csrf_token_for_form("/sightings/edit")
        sighting_date = datetime.datetime.today().strftime(Sighting.DATE_DISPLAY_FORMAT)
        location_id = self._get_random_location_id()
        category_id = self._get_random_category_id()
        species_id = self._get_random_species_id(category_id)
        self.client.post("/sightings/edit", data={
            "date": sighting_date,
            "location": str(location_id),
            "category": str(category_id),
            "species": str(species_id),
            "number": "1",
            "gender": "0",
            "with_young": "0",
            "notes": "",
            "csrf_token": csrf_token
        })

    @task
    def list_conservation_status_schemes(self):
        """
        Task to simulate listing the conservation status schemes
        """
        self.client.get("/status/list")

    @task
    def show_life_list(self):
        """
        Task to simulate showing the life list for a category
        """
        csrf_token = self._get_csrf_token_for_form("/life_list/list")
        category_id = self._get_random_category_id()
        self.client.post("/life_list/list", data={
            "category": str(category_id),
            "csrf_token": csrf_token
        })

    @task
    def list_recent_background_jobs(self):
        """
        Task to simulate listing the recent background jobs
        """
        self.client.get("/jobs/list")

    def _login(self):
        """
        Log in using the test account
        """
        csrf_token = self._get_csrf_token_for_form("/auth/login")
        self.client.post("/auth/login", data={
            "username": TEST_USER_NAME,
            "password": TEST_PASSWORD,
            "csrf_token": csrf_token
        })

    def _get_csrf_token_for_form(self, url):
        """
        Request a page containing a form and return the CSRF token from it

        :param url: URL for the page containing the form
        :return: CSFR token
        """
        response = self.client.get(url)
        form_data = BeautifulSoup(response.text, "html.parser")
        csrf_token_field = form_data.find(attrs={"name": "csrf_token"})
        return csrf_token_field["value"]

    def _get_random_location_id(self):
        """
        Return a random location ID for an existing location
        """
        index = randrange(0, len(self._locations))
        return self._locations[index].id

    def _get_random_category_id(self):
        """
        Return a random category ID for an existing category
        """
        index = randrange(0, len(self._categories))
        return self._categories[index].id

    @staticmethod
    def _get_random_species_id(category_id):
        """
        Return a random species ID for species in the specified category

        :param category_id: Category ID from which to select a species
        """
        species = list_species(category_id)
        index = randrange(0, len(species))
        return species[index].id

    def _get_name(self, prefix):
        """
        Construct a unique name for a new record with the specified prefix

        :param prefix: Prefix indicating the record type
        :return: Unique record name
        """
        return f"{prefix} - {id(self)} - {int(time.time())}"
