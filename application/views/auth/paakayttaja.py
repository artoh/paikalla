from application import app, db
from flask import render_template, request, url_for, redirect, flash
from application.forms.auth import LuoKayttajaForm
from flask_login import login_user
from application.models.henkilo import Henkilo


@app.route("/aloita")
def auth_paakayttaja():
    """Pääkäyttäjän luontilomakkeen näyttäminen, kun tietokanta on tyhjä"""
    if Henkilo.query.first() :
        return redirect(  url_for("auth_login"))

    form = LuoKayttajaForm()
    return  render_template("auth/paakayttaja.html", form = form)


@app.route("/aloita", methods=["POST"])
def auth_luo_paakayttaja():
    """Pääkäyttäjän luominen tyhjäään tietokantaan"""
    if Henkilo.query.first() :
        return redirect( url_for("auth_login"))

    form = LuoKayttajaForm(request.form)

    if not form.validate():
        return render_template("auth/paakayttaja.html", form=form)

    henkilo = form.henkilo()
    henkilo.toimihenkilo = True
    db.session.add(henkilo)
    db.session.commit()
    login_user(henkilo)
    flash("Pääkäyttäjän käyttäjätunnus luotu".format(henkilo.etunimi), "info")
    return redirect( url_for("henkilotiedot_index") )
