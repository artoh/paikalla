from application import app, db
from flask import render_template, request, url_for, redirect, flash
from application.models import Ryhma, Ryhmassa, Henkilo
from datetime import datetime, timedelta
from application.forms.kokoukset import KokousTiedotForm, KokousSarjaForm
from application.models import Kokous

@app.template_filter("menneet_kokoukset")
def filter_menneet_kokoukset(lista):
    uusilista = []
    for kokous in lista:
        if kokous.paattyy <= datetime.now() :
            uusilista.append(kokous)
    return uusilista

@app.route("/ryhmat/<ryhma_id>/menneet")
def ryhmat_menneet(ryhma_id):
    ryhma = Ryhma.query.get(ryhma_id)
    return render_template("ryhmat/menneet.html", ryhma=ryhma)