import threading
from typing import Optional
from werkzeug.serving import make_server


class FlaskAppRunner(threading.Thread):
    def __init__(self, host, port, flask_app):
        """
        Initialiser

        :param host: Hostname to serve on
        :param port: Port number to serve on
        :param flask_app: The Flask application to run
        """
        threading.Thread.__init__(self)
        self._exception = None
        self._host = host
        self._port = port
        self._server = make_server(host, port, flask_app)
        self._context = flask_app.app_context()
        self._context.push()

    def run(self, *args, **kwargs):
        """
        Run the web site on a background thread

        :param args: Variable positional arguments
        :param kwargs: Variable keyword arguments
        """
        try:
            self._server.serve_forever()
        except BaseException as e:
            # If we get an error during the run, capture it. join(), below, then raises it in the calling
            # thread
            self._exception = e

    def join(self, timeout: Optional[float] = ...) -> None:
        """
        If we have an exception, raise it in the calling thread when joined
        """
        threading.Thread.join(self)
        if self._exception:
            raise self._exception

    def stop_server(self):
        """
        Stop the Flask application
        """
        self._server.shutdown()

    def make_url(self, relative_url):
        """
        Return the absolute URL given a URL that's relative to the root of the site

        :param relative_url: Relative URL
        :return: Absolute URL corresponding to the relative URL
        """
        return f"http://{self._host}:{self._port}/{relative_url}"
