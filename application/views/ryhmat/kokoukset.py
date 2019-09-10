from application import app, db
from flask import render_template, request, url_for, redirect, flash
from application.models import Ryhma, Ryhmassa, Henkilo
from datetime import datetime
from application.forms.kokoukset import KokousTiedotForm, KokousSarjaForm

@app.route("/ryhmat/<ryhma_id>/kokoukset")
def ryhmat_kokoukset(ryhma_id):
    ryhma = Ryhma.query.get(ryhma_id)
    return render_template("ryhmat/kokoukset.html", ryhma=ryhma)

@app.route("/ryhmat/<ryhma_id>/kokoukset/uusi")
def ryhmat_kokoukset_uusi(ryhma_id):
    ryhma = Ryhma.query.get(ryhma_id)
    form = KokousTiedotForm()
    return render_template("ryhmat/uusikokous.html", ryhma=ryhma, form=form)

@app.route("/ryhmat/<ryhma_id>/kokoukset/", methods=["POST"])
def ryhmat_luo_kokous(ryhma_id):
    return redirect( url_for("ryhmat_kokoukset", ryhma_id=ryhma_id) )

@app.route("/ryhmat/<ryhma_id>/kokoukset/uusisarja")
def ryhmat_kokoukset_uusisarja(ryhma_id):
    ryhma = Ryhma.query.get(ryhma_id)
    form = KokousSarjaForm()
    return render_template("ryhmat/uusikokous.html", ryhma=ryhma, form=form)
