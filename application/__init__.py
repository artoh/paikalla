from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
Bootstrap(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///paikalla.db"
app.config["SQLALCHEMY_ECHO"] = True

# SECRET_KEY tarvitaan viestien näyttämiseen
app.config["SECRET_KEY"] = os.urandom(12).hex()

db = SQLAlchemy(app)

from application import models
from application import views

db.create_all()
