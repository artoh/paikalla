from application import app, db
from flask import render_template, request, url_for, redirect, flash
from application.models import Ryhma
from application.forms.ryhmat import RyhmaTiedotForm

@app.route("/")
def tilapainenjuuri():
    flash("Tervetuloa!","primary")
    return redirect( url_for("ryhmat_index"))

@app.route("/ryhmat/")
def ryhmat_index():
    if( "aktiiviset" in request.args.keys()) :
        ryhmat = Ryhma.query.filter_by(paattynyt=False).order_by(Ryhma.nimi).all()
    elif( "paattyneet" in request.args.keys()) :
        ryhmat = Ryhma.query.filter_by(paattynyt=True).order_by(Ryhma.nimi).all()
    else:
        ryhmat = Ryhma.query.order_by(Ryhma.nimi).all()
    return render_template("ryhmat/lista.html", ryhmat = ryhmat )


@app.route("/ryhmat/uusi/")
def ryhmat_uusi():
    return render_template("ryhmat/uusi.html", form = RyhmaTiedotForm())


@app.route("/ryhmat/", methods=["POST"])
def ryhmat_luo():
    form = RyhmaTiedotForm( request.form)

    if not form.validate() :
        return render_template("ryhmat/uusi.html", form=form)

    ryhma = Ryhma()
    form.tallenna(ryhma)
    db.session.add(ryhma )
    db.session.commit()

    flash("Ryhmä " + ryhma.nimi + " lisätty", "success")
    return redirect( url_for("ryhmat_tiedot", ryhma_id=ryhma.id) )


@app.route("/ryhmat/<ryhma_id>/tiedot/")
def ryhmat_tiedot(ryhma_id) :
    ryhma = Ryhma.query.get(ryhma_id)
    form = RyhmaTiedotForm()
    form.lataa(ryhma)

    return render_template("ryhmat/tiedot.html", ryhma=ryhma, form=form )


@app.route("/ryhmat/<ryhma_id>/tiedot/", methods=["POST"])
def ryhmat_paivita(ryhma_id) :
    form = RyhmaTiedotForm( request.form )
    ryhma = Ryhma.query.get(ryhma_id)

    if not form.validate() :
        return render_template("ryhmat/tiedot.html", ryhma=ryhma, form=form)

    form.tallenna( ryhma )
    db.session.commit()

    flash("Ryhmä " + ryhma.nimi + " tallennettu", "success")
    return redirect( url_for("ryhmat_tiedot", ryhma_id=ryhma_id ) )

@app.route("/ryhmat/<ryhma_id>/poista", methods=["POST"])
def ryhmat_poista(ryhma_id):
    ryhma = Ryhma.query.get( ryhma_id )
    flash("Ryhmä " + ryhma.nimi + " poistettu", "danger")
    db.session.delete(ryhma)
    db.session.commit()
    return redirect( url_for("ryhmat_index") )
