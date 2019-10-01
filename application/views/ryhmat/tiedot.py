from application import app, db
from flask import render_template, request, url_for, redirect, flash
from application.models import Ryhma
from application.forms.ryhmat import RyhmaTiedotForm


@app.route("/ryhmat/uusi/")
def ryhmat_uusi():
    """Uuden ryhmän luontilomakkeen näyttäminen"""
    return render_template("ryhmat/uusi.html", form = RyhmaTiedotForm())


@app.route("/ryhmat/", methods=["POST"])
def ryhmat_luo():
    """Uuden ryhmän tallentaminen tietokantaan"""
    form = RyhmaTiedotForm( request.form)

    if not form.validate():
        flash("Ole hyvä ja tarkista syöttämäsi tiedot", "danger")
        return render_template("ryhmat/uusi.html", form=form)

    ryhma = Ryhma()
    form.tallenna(ryhma)
    db.session.add(ryhma )
    db.session.commit()

    flash("Ryhmä " + ryhma.nimi + " lisätty", "success")
    return redirect( url_for("ryhmat_jasenet", ryhma_id=ryhma.id) )


@app.route("/ryhmat/<ryhma_id>/tiedot/")
def ryhmat_tiedot(ryhma_id: int):
    """Ryhmän tietojen näyttäminen"""
    ryhma = Ryhma.query.get(ryhma_id)
    form = RyhmaTiedotForm()
    form.lataa(ryhma)

    return render_template("ryhmat/tiedot.html", ryhma=ryhma, form=form )


@app.route("/ryhmat/<ryhma_id>/tiedot/", methods=["POST"])
def ryhmat_paivita(ryhma_id: int) :
    """Ryhmän tietojen päivittäminen tietokantaan"""
    form = RyhmaTiedotForm( request.form )
    ryhma = Ryhma.query.get(ryhma_id)

    if not form.validate():
        flash("Ole hyvä ja tarkista syöttämäsi tiedot", "danger")
        return render_template("ryhmat/tiedot.html", ryhma=ryhma, form=form)

    form.tallenna( ryhma )
    db.session.commit()

    flash("Ryhmä " + ryhma.nimi + " tallennettu", "success")
    return redirect( url_for("ryhmat_tiedot", ryhma_id=ryhma_id ) )
