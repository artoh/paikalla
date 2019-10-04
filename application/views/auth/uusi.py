from application import app, db
from flask import render_template, request, url_for, redirect, flash
from application.forms.auth import LuoKayttajaForm
from flask_login import login_user
from sqlalchemy.exc import IntegrityError

@app.route("/auth/uusi")
def auth_uusikayttaja():
    """Käyttäjän itserekisteröimislomakkeen näyttäminen"""
    form = LuoKayttajaForm()
    return  render_template("auth/uusikayttaja.html", form = form)


@app.route("/auth/uusi", methods=["POST"])
def auth_luo_uusikayttaja():
    """Uuden käyttäjän luominen itserekisteröitymisellä"""
    form = LuoKayttajaForm(request.form)

    if not form.validate():
        return render_template("auth/uusikayttaja.html", form=form)

    henkilo = form.henkilo()
    db.session.add(henkilo)

    try:
        db.session.commit()
    except IntegrityError:
        flash("Sähköpostiosoite on jo käytössä", "danger")
        form.email.errors.append("Sähköpostiosoite on jo käytössä");
        return render_template("auth/uusikayttaja.html", form=form)

    login_user(henkilo)
    flash("Tervetuloa {} !".format(henkilo.etunimi), "info")
    return redirect( url_for("henkilotiedot_index") )