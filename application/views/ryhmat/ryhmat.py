from application import app, db
from flask import render_template, request, url_for, redirect, flash
from application.models import Ryhma

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


@app.route("/ryhmat/<ryhma_id>/poista", methods=["POST"])
def ryhmat_poista(ryhma_id):
    ryhma = Ryhma.query.get( ryhma_id )
    flash("Ryhmä " + ryhma.nimi + " poistettu", "danger")
    db.session.delete(ryhma)
    db.session.commit()
    return redirect( url_for("ryhmat_index") )
