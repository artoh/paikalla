from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import os

app = Flask(__name__)
Bootstrap(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///paikalla.db"
app.config["SQLALCHEMY_ECHO"] = True

# SECRET_KEY tarvitaan viestien näyttämiseen
app.config["SECRET_KEY"] = os.urandom(32).hex()

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from application import models
from application import views

db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="auth_login"
login_manager.login_message = "Ole hyvä ja kirjaudu uudelleen"

from application.models.henkilo import Henkilo

@login_manager.user_loader
def load_user(user_id):
    return  Henkilo.query.get(user_id)

