"""
This module defines a base class for CSV data exchange helpers that complete on a background thread. The
CSV files have the following columns:

+-------------------+--------------------------------------------------------------------------+
| Column            | Contents                                                                 |
+-------------------+--------------------------------------------------------------------------+
| Species           | Common name of the species                                               |
+-------------------+--------------------------------------------------------------------------+
| Scientific Name   | Scientific name of the species                                           |
+-------------------+--------------------------------------------------------------------------+
| Category          | Category to which the species belongs                                    |
+-------------------+--------------------------------------------------------------------------+
| Number            | Number of individuals seen or 0 if not counted                           |
+-------------------+--------------------------------------------------------------------------+
| Gender            | Gender of the individuals seen - Unkown, Male, Female or Both            |
+-------------------+--------------------------------------------------------------------------+
| WithYoung         | Yes or No, indicating whether young were also seen                       |
+-------------------+--------------------------------------------------------------------------+
| Date              | Date of the sighting in DD/MM/YYYY format                                |
+-------------------+--------------------------------------------------------------------------+
| Location          | Name of the location where the sighting was made                         |
+-------------------+--------------------------------------------------------------------------+
| Address           | Street address for the location                                          |
+-------------------+--------------------------------------------------------------------------+
| City              | City for the location                                                    |
+-------------------+--------------------------------------------------------------------------+
| County            | County for the location                                                  |
+-------------------+--------------------------------------------------------------------------+
| Postcode          | Postcode for the location                                                |
+-------------------+--------------------------------------------------------------------------+
| Latitude          | Latitude for the location  in decimal format                             |
+-------------------+--------------------------------------------------------------------------+
| Longitude         | Longitude for the location  in decimal format                            |
+-------------------+--------------------------------------------------------------------------+
| Notes             | Sighting notes                                                           |
+-------------------+--------------------------------------------------------------------------+
"""

from .data_exchange_helper_base import DataExchangeHelperBase


class SightingsDataExchangeHelperBase(DataExchangeHelperBase):
    COLUMN_NAMES = [
        'Species',
        'Scientific Name',
        'Category',
        'Number',
        'Gender',
        'WithYoung',
        'Date',
        'Location',
        'Address',
        'City',
        'County',
        'Postcode',
        'Country',
        'Latitude',
        'Longitude',
        'Notes'
    ]

    def __init__(self, action, user):
        """
        Initialiser

        :param action: Callable to perform the data exchange operation
        :param user: Current user
        """
        super().__init__(action, user)

    @classmethod
    def get_field_name(cls, index):
        """
        Return the name of the column at the specified index

        :param index: Column index
        :return: Column name
        """
        return cls.COLUMN_NAMES[index]
