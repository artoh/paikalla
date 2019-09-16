from flask import render_template, request, redirect, url_for

from application import app, bcrypt
from application.models import Henkilo

from flask_login import login_user, logout_user

@app.route("/", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        if not Henkilo.query.first() :
            # Tyhjä tietokanta
            return redirect( url_for("auth_paakayttaja"))

        return render_template("auth/login.html", email="")

    email = request.form.get("email")
    salasanaTiiviste = request.form.get("salasana")

    kayttaja = Henkilo.query.filter_by(email=email).first()
    if not kayttaja:
        return render_template("auth/login.html",
                               virhe = "Et ole rekisteröitynyt tällä sähköpostiosoitteella.",
                               email=email)

    if( bcrypt.check_password_hash( kayttaja.salasana, salasanaTiiviste )) :
        login_user(kayttaja)
        return redirect(url_for("ilmoittautumiset_index"))
    else:
        return render_template("auth/login.html",
                               virhe = "Virheellinen salasana",
                               email=email)

@app.route("/logout")
def auth_logout():
    logout_user()
    return redirect( url_for("auth_login") )
