from application import app, login_manager
from application.models.ryhma import Ryhma
from flask import render_template, request
from datetime import date
from dateutil.parser import parse
from application.helpers.autorisointi import ryhma_autorisaatio

@app.route("/ryhmat/<ryhma_id>/ryhmatilasto")
def ryhmat_tilasto(ryhma_id : int):
    """Näyttää ryhmän tilaston ja jäsenten aktiivisuuden"""
    if not ryhma_autorisaatio(ryhma_id):
        return login_manager.unauthorized()

    ryhma = Ryhma.query.get(ryhma_id)

    mista = parse( request.args.get("mista", date.today().strftime("%Y-01-01") ) )
    mihin = parse( request.args.get("mihin", date.today().strftime("%Y-%m-%d") ) )

    return render_template("ryhmat/tilasto.html", ryhma=ryhma, mista=mista, mihin=mihin, tiedot=ryhma.ryhmantilasto(mista, mihin))
