from application import app, db
from flask import render_template, request, url_for, redirect, flash
from application.models import Ryhma, Ryhmassa, Henkilo
from datetime import datetime


@app.route("/ryhmat/<ryhma_id>/ohjaajat")
def ryhmat_ohjaajat(ryhma_id):
    ryhma = Ryhma.query.get(ryhma_id)
    ohjaajat = ryhma.ohjaajat()

    kaikkiaikuiset = Henkilo.query.filter_by(aikuinen=True).order_by(Henkilo.sukunimi)
    aikuiset = []
    for aikuinen in kaikkiaikuiset:
        if aikuinen not in ohjaajat:
            aikuiset.append(aikuinen)

    return render_template("ryhmat/ohjaajat.html", ryhma=ryhma, aikuiset=aikuiset)


@app.route("/ryhmat/<ryhma_id>/linkitaohjaaja", methods=["POST"])
def ryhmat_linkita_ohjaaja(ryhma_id):
    ryhmassa = Ryhmassa(ryhmaId=ryhma_id, jasenId=request.form.get("linkita"), ohjaaja=True)
    ryhmassa.alkaen = datetime.today()
    db.session.add(ryhmassa)
    db.session.commit()
    return redirect( url_for("ryhmat_ohjaajat", ryhma_id=ryhma_id) )

@app.route("/ryhmat/<ryhma_id>/jasenet")
def ryhmat_jasenet(ryhma_id):
    ryhma = Ryhma.query.get(ryhma_id)
    ohjaajat = ryhma.ohjaajat()

    ohjaajat = ryhma.ohjaajat()
    jasenet = ryhma.jasenet()

    kaikkijasenet = Henkilo.query.order_by(Henkilo.sukunimi)
    eiryhmassa = []
    for henkilo in kaikkijasenet:
        if henkilo not in ohjaajat and henkilo not in jasenet:
            eiryhmassa.append(henkilo)

    return render_template("ryhmat/jasenet.html", ryhma=ryhma, jasenet=eiryhmassa)


@app.route("/ryhmat/<ryhma_id>/linkitajasen", methods=["POST"])
def ryhmat_linkita_jasen(ryhma_id):
    ryhmassa = Ryhmassa(ryhmaId=ryhma_id, jasenId=request.form.get("linkita"), ohjaaja=False)
    ryhmassa.alkaen = datetime.today()
    db.session.add(ryhmassa)
    db.session.commit()
    return redirect( url_for("ryhmat_jasenet", ryhma_id=ryhma_id) )
