from application import app, db
from flask import render_template, request, url_for, redirect, flash
from application.models import Ryhma

@app.route("/ryhmat/")
def ryhmat_index():
    if( "aktiiviset" in request.args.keys()) :
        ryhmat = Ryhma.lista(Ryhma.AKTIIVISETRYHMAT)
    elif( "paattyneet" in request.args.keys()) :
        ryhmat = Ryhma.lista(Ryhma.PAATTYNEETRYHMAT)
    else:
        ryhmat = Ryhma.lista(Ryhma.KAIKKIRYHMAT)
    return render_template("ryhmat/lista.html", ryhmat = ryhmat )


@app.route("/ryhmat/<ryhma_id>/poista", methods=["POST"])
def ryhmat_poista(ryhma_id):
    ryhma = Ryhma.query.get( ryhma_id )
    flash("Ryhmä " + ryhma.nimi + " poistettu", "danger")
    db.session.delete(ryhma)
    db.session.commit()
    return redirect( url_for("ryhmat_index") )
