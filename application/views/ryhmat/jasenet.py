from application import app, db, login_manager
from flask import render_template, request, url_for, redirect
from application.models import Ryhma, Ryhmassa, Henkilo
from datetime import datetime
from application.helpers.autorisointi import ryhma_autorisaatio


@app.route("/ryhmat/<ryhma_id>/ryhmassa")
def ryhmat_jasenet(ryhma_id: int):
    """Ryhmän jäsenluettelon näyttäminen"""
    if not ryhma_autorisaatio(ryhma_id):
        return login_manager.unauthorized();

    ryhma = Ryhma.query.get(ryhma_id)
    jasenet = ryhma.jasenet()

    ryhmassaidt = []
    for jasen in jasenet :
        ryhmassaidt.append( jasen["henkiloId"] )

    # Uusien jäsenten lisäämistoimintoa (chosen-select) varten haetaan kaikkien
    # niiden henkilöiden nimet, jotka eivät ole ryhmässä,
    # Näin ylläpitäjä voi lisätä sellaisenkin jäsnen, joka ei täytä ikävaatimusta,
    # tai jäsenen ryhmään, joka on jo täysi.
    kaikkijasenet = Henkilo.query.filter(Henkilo.jasenyysalkoi.isnot(None),
                                         Henkilo.jasenyyspaattyi == None).order_by(Henkilo.sukunimi)
    eiryhmassa = []
    for henkilo in kaikkijasenet:
        if henkilo.id not in ryhmassaidt:
            eiryhmassa.append(henkilo)

    return render_template("ryhmat/jasenet.html", ryhma=ryhma, eiryhmassa=eiryhmassa, jasenet=jasenet)


@app.route("/ryhmat/<ryhma_id>/linkitaohjaaja", methods=["POST"])
def ryhmat_linkita_ohjaaja(ryhma_id: int):
    """Lisää ryhmään ohjaaja"""
    if not ryhma_autorisaatio(ryhma_id):
        return login_manager.unauthorized();
    ryhmassa = Ryhmassa(ryhmaId=ryhma_id, jasenId=request.form.get("linkita"), ohjaaja=True)
    ryhmassa.alkaen = datetime.today()
    db.session.add(ryhmassa)
    db.session.commit()
    return redirect( url_for("ryhmat_jasenet", ryhma_id=ryhma_id) )


@app.route("/ryhmat/<ryhma_id>/linkitajasen", methods=["POST"])
def ryhmat_linkita_jasen(ryhma_id: int):
    """Lisää ryhmään jäsenen"""
    if not ryhma_autorisaatio(ryhma_id):
        return login_manager.unauthorized();
    ryhmassa = Ryhmassa(ryhmaId=ryhma_id, jasenId=request.form.get("linkita"), ohjaaja=False)
    ryhmassa.alkaen = datetime.today()
    db.session.add(ryhmassa)
    db.session.commit()
    return redirect( url_for("ryhmat_jasenet", ryhma_id=ryhma_id) )


@app.route("/ryhmat/poistajasenyys/<ryhmassa_id>", methods=["POST"])
def ryhmat_erota_jasen(ryhmassa_id: int):
    """Merkitsee ryhmän jäsenneen eronneeksi.
       Jotta tilastoinnit yms. onnistuvat, ei jäsenyyttä tuhota, vaan siihen
       merkitään loppumspäivä,"""
    ryhmassa=Ryhmassa.query.get(ryhmassa_id)
    if not ryhma_autorisaatio(ryhmassa.ryhmaid):
        return login_manager.unauthorized();
    ryhmassa.paattyen=datetime.today()
    db.session.commit()
    return redirect(url_for("ryhmat_jasenet", ryhma_id=ryhmassa.ryhmaid))


@app.route("/ryhmat/ryhmassa/<ryhmassa_id>")
def ryhmat_jasen_tiedot(ryhmassa_id: int):
    """Näyttää yksittäisen jäsenen tiedot.
       Alaikäiselle näytetään myös huoltajien yhteystiedot."""
    ryhmassa = Ryhmassa.query.get(ryhmassa_id)
    if not ryhma_autorisaatio(ryhmassa.ryhmaid):
        return login_manager.unauthorized();
    return render_template("ryhmat/jasentiedot.html",jasenyys=ryhmassa, ryhma=ryhmassa.ryhma)