from application import app, admin_required
from application.models.ryhma import Ryhma
from flask import render_template, request
from datetime import date
from dateutil.parser import parse

@app.route("/yleistilasto")
@admin_required()
def yleistilasto():
    mista = parse( request.args.get("mista", date.today().strftime("%Y-01-01") ) )
    mihin = parse( request.args.get("mihin", date.today().strftime("%Y-%m-%d") ) )

    return render_template("tilasto/tilasto.html", mista=mista, mihin=mihin,
                    ryhmat=Ryhma.yhteistilasto(mista, mihin))
