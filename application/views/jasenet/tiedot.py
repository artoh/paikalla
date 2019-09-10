from application import app, db
from flask import render_template, request, url_for, redirect, flash
from application.models import Henkilo
from application.forms.jasenet import HenkiloTiedotAdminilleForm, HenkiloTiedotForm
from datetime import datetime

@app.route("/jasenet/")
def jasenet_index() :
    return render_template("jasenet/lista.html", jasenet = Henkilo.query.order_by(Henkilo.sukunimi, Henkilo.etunimi)  )


@app.route("/jasenet/uusi")
def jasenet_uusi() :
    form = HenkiloTiedotAdminilleForm()
    form.jasenyysAlkoi.data = datetime.now()
    return render_template("jasenet/uusi.html", form = form)


@app.route("/jasenet", methods=["POST"])
def jasenet_luo() :
    form = HenkiloTiedotAdminilleForm( request.form )

    if not form.validate() :
        return render_template("jasenet/uusi.html", form = form)

    henkilo = Henkilo()
    form.tallenna( henkilo )
    db.session.add( henkilo )
    db.session.commit()

    return redirect( url_for("jasenet_tiedot", henkilo_id=henkilo.id))


@app.route("/jasenet/<henkilo_id>/tiedot/")
def jasenet_tiedot(henkilo_id) :
    henkilo = Henkilo.query.get(henkilo_id)
    form = HenkiloTiedotAdminilleForm()
    form.lataa(henkilo)


    return render_template("jasenet/tiedot.html", jasen=henkilo, form=form )


@app.route("/jasenet/<henkilo_id>/tiedot", methods=["POST"])
def jasenet_paivita(henkilo_id):
    form = HenkiloTiedotAdminilleForm( request.form)
    henkilo = Henkilo.query.get(henkilo_id)

    if not form.validate():
        return render_template("jasenet/tiedot", jasen=henkilo, form=form)

    form.tallenna(henkilo)
    db.session.commit()

    flash("Henkilön " + henkilo.etunimi + " " + henkilo.sukunimi + " tiedot tallennettu", "success")
    return redirect( url_for("jasenet_tiedot", henkilo_id=henkilo_id) )





@app.route("/jasenet/<henkilo_id>/poista", methods=["POST"])
def jasenet_poista(henkilo_id):
    henkilo = Henkilo.query.get( henkilo_id )
    flash( henkilo.etunimi + " " + henkilo.sukunimi + " poistettu", "danger")
    db.session.delete(henkilo)
    db.session.commit()
    return redirect( url_for("jasenet_index") )