from application import app, db, login_manager
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_required
from .autorisointi import kayttaja_autorisointi

@app.route("/ilmoittautumiset")
@login_required
def ilmoittautumiset_index():
    return render_template("mina/ilmoittautumiset.html")

@app.route("/ilmoittautumiset/uusilista/<henkilo_id>")
def ilmoittautumiset_uusi_lista(henkilo_id):
    henkilo = kayttaja_autorisointi(henkilo_id)
    if not henkilo:
        return login_manager.unauthorized()
    return render_template("mina/lista.html", henkilo=henkilo)