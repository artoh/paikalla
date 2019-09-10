from application import app, db
from flask import render_template, request, url_for, redirect, flash
from application.models import Ryhma, Ryhmassa, Henkilo
from datetime import datetime

@app.route("/ryhmat/<ryhma_id>/jasenet")
def ryhmat_jasenet(ryhma_id):
    ryhma = Ryhma.query.get(ryhma_id)
    jasenyydet = ryhma.jasenyydet()

    ryhmassaidt = []
    for jasenyys in jasenyydet :
        ryhmassaidt.append(jasenyys["henkiloId"])

    kaikkijasenet = Henkilo.query.order_by(Henkilo.sukunimi)
    eiryhmassa = []
    for henkilo in kaikkijasenet:
        if henkilo.id not in ryhmassaidt:
            eiryhmassa.append(henkilo)

    return render_template("ryhmat/jasenet.html", ryhma=ryhma, eiryhmassa=eiryhmassa, jasenyydet=ryhma.jasenyydet())


@app.route("/ryhmat/<ryhma_id>/linkitaohjaaja", methods=["POST"])
def ryhmat_linkita_ohjaaja(ryhma_id):
    ryhmassa = Ryhmassa(ryhmaId=ryhma_id, jasenId=request.form.get("linkita"), ohjaaja=True)
    ryhmassa.alkaen = datetime.today()
    db.session.add(ryhmassa)
    db.session.commit()
    return redirect( url_for("ryhmat_jasenet", ryhma_id=ryhma_id) )


@app.route("/ryhmat/<ryhma_id>/linkitajasen", methods=["POST"])
def ryhmat_linkita_jasen(ryhma_id):
    ryhmassa = Ryhmassa(ryhmaId=ryhma_id, jasenId=request.form.get("linkita"), ohjaaja=False)
    ryhmassa.alkaen = datetime.today()
    db.session.add(ryhmassa)
    db.session.commit()
    return redirect( url_for("ryhmat_jasenet", ryhma_id=ryhma_id) )

@app.route("/ryhmat/poistajasenyys/<ryhmassa_id>", methods=["POST"])
def ryhmat_erota_jasen(ryhmassa_id):
    ryhmassa=Ryhmassa.query.get(ryhmassa_id)
    ryhmassa.paattyen=datetime.today()
    db.session.commit()
    return redirect(url_for("ryhmat_jasenet", ryhma_id=ryhmassa.ryhma))