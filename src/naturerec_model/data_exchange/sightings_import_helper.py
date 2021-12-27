"""
This module implements a helper that will import sightings from a CSV format file on a background thread
"""

import csv
import os
from .sightings_data_exchange_helper_base import SightingsDataExchangeHelperBase
from ..model import get_data_path
from ..logic.sightings import list_sightings


class SightingsImportHelper(SightingsDataExchangeHelperBase):
    def __init__(self, f):
        """
        Initialiser

        :param f: IO stream (result of open() or a FileStorage object)
        """
        super().__init__(self.import_sightings)
        self._file = f

    def import_sightings(self):
        pass
