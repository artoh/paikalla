from application import app, db, admin_required
from flask import render_template, request, url_for, redirect, flash
from application.models import Ryhma


@app.route("/ryhmat/")
@admin_required()
def ryhmat_index():
    """Ryhmien luettelon näyttäminen"""
    if( "aktiiviset" in request.args.keys()) :
        ryhmat = Ryhma.lista(Ryhma.AKTIIVISETRYHMAT)
    elif( "paattyneet" in request.args.keys()) :
        ryhmat = Ryhma.lista(Ryhma.PAATTYNEETRYHMAT)
    else:
        ryhmat = Ryhma.lista(Ryhma.KAIKKIRYHMAT)
    return render_template("ryhmat/lista.html", ryhmat = ryhmat )


@app.route("/ryhmat/<ryhma_id>/poista", methods=["POST"])
@admin_required()
def ryhmat_poista(ryhma_id: int):
    """Ryhmän poistaminen tietokannasta"""
    ryhma = Ryhma.query.get( ryhma_id )
    flash("Ryhmä " + ryhma.nimi + " poistettu", "danger")
    db.session.delete(ryhma)
    db.session.commit()
    return redirect( url_for("ryhmat_index") )
