from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///paikalla.db"
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

from application import models
from application import views


db.create_all()
