"""
The jobs blueprint supplies view functions and templates for background job management
"""

import datetime
from flask import Blueprint, render_template
from naturerec_model.logic import list_job_status


jobs_bp = Blueprint("jobs", __name__, template_folder='templates')


@jobs_bp.route("/list", methods=["GET", "POST"])
def list_recent():
    """
    Show the page that lists recent background jobs

    :return: The HTML for the job listing page
    """

    # Find matching job status records
    from_date = datetime.datetime.today().date() - datetime.timedelta(days=1)
    job_statuses = list_job_status(from_date=from_date)

    # Serve the page
    return render_template("jobs/list.html",
                           job_statuses=job_statuses)
