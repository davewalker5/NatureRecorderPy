"""
This module implements a Flask-based web application based on the functionality provided by the "naturerec_model"
package.

The site is not responsive but the Bootstrap customizer has been used to generate a cut-down version of bootstrap
to provide button and form element styling.
"""

import os
from flask import Flask, render_template

app = Flask("Nature Recorder",
            static_folder=os.path.join(os.path.dirname(__file__), "static"),
            template_folder=os.path.join(os.path.dirname(__file__), "templates"))

@app.route("/")
def home():
    """
    Serve the home page for the site

    :return: Rendered home page template
    """
    return render_template("home.html")
