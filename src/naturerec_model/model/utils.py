"""
Data file management utilities
"""

import os


def get_project_path():
    """
    Return the path to the root folder of the project

    :return: The path to the project root folder
    """
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def get_data_path():
    """
    Return the path to the project's data folder

    :return: The path to the data folder
    """
    data_folder = os.environ["NATURE_RECORDER_DATA_FOLDER"] if "NATURE_RECORDER_DATA_FOLDER" in os.environ else None
    if not data_folder:
        data_folder = os.path.join(get_project_path(), "data")
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
    return data_folder
