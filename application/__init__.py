from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///paikalla.db"
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from application import models
from application import views


db.create_all()
