from application import app
from flask import render_template
from application.models import Henkilo


@app.route("/jasenet/<henkilo_id>/ryhmissa")
def jasenet_ryhmat(henkilo_id: int):
    """Näyttää henkilön ryhmäjäsenyydet"""
    henkilo = Henkilo.query.get(henkilo_id)
    return render_template("jasenet/ryhmat.html", jasen=henkilo)
