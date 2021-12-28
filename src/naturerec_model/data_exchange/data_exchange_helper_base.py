"""
This module defines a base class for data exchange helpers that complete on a background thread
"""

import threading
from typing import Optional
from ..logic import create_category, get_category
from ..logic import create_species


class DataExchangeHelperBase(threading.Thread):
    def __init__(self, action):
        """
        Initialiser

        :param action: Callable to perform the data exchange operation
        """
        threading.Thread.__init__(self)
        self._action = action
        self._exception = None

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

    def join(self, timeout: Optional[float] = ...) -> None:
        """
        If we have an exception, raise it in the calling thread when joined
        """
        threading.Thread.join(self)
        if self._exception:
            raise self._exception

    @staticmethod
    def create_species(category_name, species_name):
        """
        Ensure the species with the specified name exists in the specified category

        :param category_name: Name of the category to which the species belongs
        :param species_name: Name of the species
        """
        tidied_category_name = " ".join(category_name.split()).title()
        tidied_species_name = " ".join(species_name.split()).title()

        # See if the category exists and, if not, create it and the species
        try:
            category = get_category(tidied_category_name)
        except ValueError:
            category = create_category(tidied_category_name)
            return create_species(category.id, tidied_species_name).id

        # See if the species exists against the existing category. If so, just return its ID
        species_ids = [species.id for species in category.species if species.name == tidied_species_name]
        if len(species_ids):
            return species_ids[0]

        # Doesn't exist so create it and return its ID
        return create_species(category.id, tidied_species_name).id
