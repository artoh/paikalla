from application import app, db
from flask import render_template, request, url_for, redirect, flash
from application.models import Henkilo

@app.route("/jasenet/<henkilo_id>/ryhmissa")
def jasenet_ryhmat(henkilo_id):
    henkilo = Henkilo.query.get(henkilo_id)
    return render_template("jasenet/ryhmat.html", jasen=henkilo)
