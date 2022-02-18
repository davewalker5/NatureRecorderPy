"""
Flask configuration
"""

import os
from dotenv import load_dotenv

basedir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
env_file = os.path.join(basedir, "data", ".env")
load_dotenv(env_file)


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')


class ProductionConfig(BaseConfig):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SERVER_NAME = "0.0.0.0"


class DevelopmentConfig(BaseConfig):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SERVER_NAME = "127.0.0.1:5000"
