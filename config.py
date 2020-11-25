"""Flask config."""
from os import environ


SECRET_KEY = environ.get('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False
