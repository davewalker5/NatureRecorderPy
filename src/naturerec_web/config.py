"""
Flask configuration
"""

import os
from dotenv import load_dotenv

basedir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if "NATURE_RECORDER_DATA_FOLDER" in os.environ:
    env_file = os.path.join(os.environ["NATURE_RECORDER_DATA_FOLDER"], ".env")
else:
    env_file = os.path.join(basedir, "data", ".env")
load_dotenv(env_file)


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')


class ProductionConfig(BaseConfig):
    TESTING = False


class DevelopmentConfig(BaseConfig):
    TESTING = True
