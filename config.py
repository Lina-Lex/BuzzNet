"""Flask config."""
from decouple import config


class Config:
    """Base config."""
    DEBUG = False
    TESTING = False
    FLASK_APP = 'wsgi.py'
    FLASK_ENV = config('FLASK_ENV')
    SECRET_KEY = config('SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Database
    SQLALCHEMY_DATABASE_URI = config("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    TESTING = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True
