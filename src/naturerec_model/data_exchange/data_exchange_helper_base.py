"""
This module defines a base class for data exchange helpers that complete on a background thread
"""

import threading
import datetime
from typing import Optional
from collections import namedtuple
from ..logic import create_category, get_category
from ..logic import create_species
from ..logic import create_job_status, complete_job_status


class DataExchangeHelperBase(threading.Thread):
    JOB_NAME = "Data Exchange Job"

    def __init__(self, action, user):
        """
        Initialiser

        :param action: Callable to perform the data exchange operation
        :param user: Current user
        """
        threading.Thread.__init__(self)
        self._action = action

        # The following's done to create a local user class on the fly, as the "current_user" object that's
        # passed in from e.g. the Flask UI may not be valid when the job comes to complete as the page will
        # have been served
        DataExchangeUser = namedtuple("DataExchangeUser", "id")
        self._user = DataExchangeUser(id=user.id)

        self._exception = None
        self._job_status_id = None

    def run(self, *args, **kwargs):
        """
        Import conservation status schemes and ratings from a CSV file on a background thread

        :param args: Variable positional arguments
        :param kwargs: Variable keyword arguments
        """
        try:
            self._action()
        except BaseException as e:
            # If we get an error during import, capture it. join(), below, then raises it in the calling
            # thread
            self._exception = e

        self.complete_job_status()

    def join(self, timeout: Optional[float] = ...) -> None:
        """
        If we have an exception, raise it in the calling thread when joined
        """
        threading.Thread.join(self)
        if self._exception:
            raise self._exception

    def create_species(self, category_name, species_name, scientific_name):
        """
        Ensure the species with the specified name exists in the specified category

        :param category_name: Name of the category to which the species belongs
        :param species_name: Common name of the species
        :param scientific_name: Scientific name of the species
        """
        tidied_category_name = " ".join(category_name.split()).title()
        tidied_species_name = " ".join(species_name.split()).title()
        tidied_scientific_name = " ".join(scientific_name.split()).title() if scientific_name != None else None

        # See if the category exists and, if not, create it and the species
        try:
            category = get_category(tidied_category_name)
        except ValueError:
            category = create_category(tidied_category_name, self._user)
            return create_species(category.id, tidied_species_name, tidied_scientific_name, self._user).id

        # See if the species exists against the existing category. If so, just return its ID
        species_ids = [species.id for species in category.species if species.name == tidied_species_name]
        if len(species_ids):
            return species_ids[0]

        # Doesn't exist so create it and return its ID
        return create_species(category.id, tidied_species_name, tidied_scientific_name, self._user).id

    def create_job_status(self):
        """
        Create a job status record for this job
        """
        self._job_status_id = create_job_status(self.JOB_NAME, repr(self), datetime.datetime.now(), self._user).id

    def complete_job_status(self):
        """
        Complete the job status record for this job
        """
        if self._job_status_id:
            error = str(self._exception) if self._exception else None
            _ = complete_job_status(self._job_status_id, datetime.datetime.now(), error, self._user)
