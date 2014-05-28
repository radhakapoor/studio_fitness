import os

SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
basedir = os.path.dirname(__file__)

SECRET_KEY = os.environ["SECRET_KEY"]