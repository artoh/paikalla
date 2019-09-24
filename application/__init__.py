from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import os
import locale

# Asetetaan paikallistus, jotta voidaan tulostaa viikonpäivät
# Tämä edellyttää lokalisaatioiden asentamista Herokuun (katso asennusohja)
locale.setlocale(locale.LC_ALL,'fi_FI.UTF-8')

app = Flask(__name__)
# flask_bootstrapia käytetään lomakkeiden muotoiluun ja generoimiseen
Bootstrap(app)


if os.environ.get("PRODUCTION"):
    # Tuotantoympäristö esim. Herokuun vietäessä, käyttää PostgreSQL:ää
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
else:
    # Paikallinen development-ympäristö, käyttää SQLiteä
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///paikalla.db"
    app.config["SQLALCHEMY_ECHO"] = True

# Keksien suojaamista tarvitaan kirjautumisessa sekä flashien näyttämisessä
app.config["SECRET_KEY"] = os.urandom(32).hex()

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="auth_login"
login_manager.login_message = "Ole hyvä ja kirjaudu uudelleen"

from application import models
from application import views

try:
    db.create_all()
except:
    pass

from application.models.henkilo import Henkilo


@login_manager.user_loader
def load_user(user_id):
    return  Henkilo.query.get(user_id)

