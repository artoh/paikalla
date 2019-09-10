from application import app, db
from flask import render_template, request, url_for, redirect, flash
from application.models import Henkilo
from application.forms.jasenet import HenkiloTiedotAdminilleForm
from datetime import datetime


@app.route("/jasenet/<henkilo_id>/huollettavat")
def jasenet_huollettavat(henkilo_id):
    henkilo = Henkilo.query.get(henkilo_id)
    kaikkilapset = Henkilo.query.filter_by(aikuinen=False).order_by(Henkilo.sukunimi)
    lapset = []
    for lapsi in kaikkilapset :
        if lapsi not in henkilo.huollettavat :
            lapset.append(lapsi)

    return render_template("jasenet/huollettavat.html", jasen=henkilo, lapset=lapset)

@app.route("/jasenet/<huoltaja_id>/linkitahuollettava", methods=["POST"])
def jasenet_linkita_huollettava(huoltaja_id):
    # Tarkistettava, ettei vielä ole huollettava
    henkilo = Henkilo.query.get(huoltaja_id)
    huollettava = Henkilo.query.get( request.form.get("linkita") )
    huollettava.huoltajat.append(henkilo)
    db.session.commit()
    return redirect(  url_for("jasenet_huollettavat", henkilo_id=huoltaja_id))


@app.route("/jasenet/<huoltaja_id>/uusihuollettava")
def jasenet_uusi_huollettava(huoltaja_id):
    huoltaja = Henkilo.query.get(huoltaja_id)
    form = HenkiloTiedotAdminilleForm()
    form.jasenyysAlkoi.data = datetime.today()
    return render_template("jasenet/uusihuollettava.html", henkilo=huoltaja, form=form)


@app.route("/jasenet/<huoltaja_id>/huollettavat", methods=["POST"])
def jasenet_luo_huollettava(huoltaja_id):
    form = HenkiloTiedotAdminilleForm( request.form )

    if not form.validate() :
        return render_template("jasenet/uusi.html", form = form)

    huoltaja = Henkilo.query.get(huoltaja_id)
    henkilo = Henkilo()
    form.tallenna( henkilo )
    henkilo.huoltajat.append(huoltaja)
    db.session.add( henkilo )
    db.session.commit()

    return redirect( url_for("jasenet_huollettavat", henkilo_id=huoltaja_id))