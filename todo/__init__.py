import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from config import basedir


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from todo import views, models