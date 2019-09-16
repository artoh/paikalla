from application import app, db
from flask import render_template, request, url_for, redirect, flash
from application.models import Ryhma, Ryhmassa, Henkilo
from datetime import datetime

@app.route("/ryhmat/<ryhma_id>/ryhmassa")
def ryhmat_jasenet(ryhma_id):
    ryhma = Ryhma.query.get(ryhma_id)
    jasenet = ryhma.jasenet()

    ryhmassaidt = []
    for jasen in jasenet :
        ryhmassaidt.append( jasen["henkiloId"] )

    kaikkijasenet = Henkilo.query.filter(Henkilo.jasenyysAlkoi.isnot(None),
                                         Henkilo.jasenyysPaattyi == None).order_by(Henkilo.sukunimi)
    eiryhmassa = []
    for henkilo in kaikkijasenet:
        if henkilo.id not in ryhmassaidt:
            eiryhmassa.append(henkilo)

    return render_template("ryhmat/jasenet.html", ryhma=ryhma, eiryhmassa=eiryhmassa, jasenet=jasenet)


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
    return redirect(url_for("ryhmat_jasenet", ryhma_id=ryhmassa.ryhmaId))

@app.route("/ryhmat/ryhmassa/<ryhmassa_id>")
def ryhmat_jasen_tiedot(ryhmassa_id):
    ryhmassa = Ryhmassa.query.get(ryhmassa_id)

    return render_template("ryhmat/jasentiedot.html",jasenyys=ryhmassa, ryhma=ryhmassa.ryhma)