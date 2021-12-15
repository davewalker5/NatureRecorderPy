"""
Data file management utilities
"""

import os


def get_data_path():
    """
    Return the path to the project's data folder

    :return: The path to the data folder
    """
    project_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    data_folder = os.path.join(project_folder, "data")
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    return data_folder
