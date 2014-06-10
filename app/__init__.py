from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from config import basedir
import os 

app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view='get_login'

from app import routes#, models


