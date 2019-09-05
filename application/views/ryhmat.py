from application import app, db
from flask import render_template, request, url_for, redirect
from application.models import Ryhma
from application.forms.ryhmaforms import RyhmaTiedotForm


@app.route("/ryhmat")
def ryhmat_index():
    return render_template("ryhmat/lista.html", ryhmat = Ryhma.query.all() )


@app.route("/ryhmat/uusi/")
def ryhmat_uusi():
    return render_template("ryhmat/uusi.html")


@app.route("/ryhmat/", methods=["POST"])
def ryhmat_luo():
    r = Ryhma(request.form.get("nimi"))

    db.session.add(r)
    db.session.commit()

    return redirect( url_for("ryhmat_index") )


@app.route("/ryhmat/<ryhma_id>/tiedot/")
def ryhmat_tiedot(ryhma_id) :
    ryhma = Ryhma.query.get(ryhma_id)
    form = RyhmaTiedotForm()
    form.tayta(ryhma)

    return render_template("ryhmat/tiedot.html", ryhma=ryhma, form=form )


@app.route("/ryhmat/<ryhma_id>/paivita/")
def ryhmat_paivita(ryhma_id) :
    return redirect( url_for("ryhmat_tiedot", ryhma_id=ryhma_id ) )
