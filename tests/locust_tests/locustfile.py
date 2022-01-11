from locust import HttpUser, task, between, events
from flask_app_runner import FlaskAppRunner
from naturerec_web import app as nature_recorder_app


flask_runner = None


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """
    Before any tests run, start the Flask application

    :param environment: Ignored
    :param kwargs: Ignored
    """
    global flask_runner
    flask_runner = FlaskAppRunner("127.0.0.1", 5000, nature_recorder_app)
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
    Demonstration Locust load test, targeting the Nature Recorder application hosted in Docker.
    To run the tests, open a terminal window, activate the virtual environment and run:

    locust -f locustfile.py
    """

    #: Simulated users will wait between 1 and 5 seconds per task
    wait_time = between(1, 5)

    @task
    def go_to_home_page(self):
        """
        Task to open the home page of the application
        """
        self.client.get("/")

    @task
    def list_species(self):
        """
        Task to simulate listing the species belonging to a selected category
        """
        self.client.post("/species/list", data={"category": "2"})
