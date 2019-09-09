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


@app.route("/jasenet/<henkilo_id>/huoltajat")
def jasenet_huoltajat(henkilo_id):
    henkilo = Henkilo.query.get(henkilo_id)
    kaikkiaikuiset = Henkilo.query.filter_by(aikuinen=True).order_by(Henkilo.sukunimi)
    aikuiset = []
    for aikuinen in kaikkiaikuiset:
        if aikuinen not in henkilo.huoltajat:
            aikuiset.append(aikuinen)

    return render_template("jasenet/huoltajat.html", jasen=henkilo, aikuiset=aikuiset)


@app.route("/jasenet/<henkilo_id>/linkitahuoltaja", methods=["POST"])
def jasenet_linkita_huoltaja(henkilo_id):
    henkilo = Henkilo.query.get(henkilo_id)
    huoltaja = Henkilo.query.get( request.form.get("linkita") )
    henkilo.huoltajat.append(huoltaja)
    db.session.commit()
    return redirect(  url_for("jasenet_huoltajat", henkilo_id=henkilo_id))

@app.route("/jasenet/<huollettava_id>/uusihuoltaja")
def jasenet_uusi_huoltaja(huollettava_id):
    huollettava = Henkilo.query.get(huollettava_id)
    form = HenkiloTiedotAdminilleForm()
    form.jasenyysAlkoi.data = datetime.today()
    form.aikuinen.data = True
    return render_template("jasenet/uusihuoltaja.html", henkilo=huollettava, form=form)


@app.route("/jasenet/<huollettava_id>/huoltajat", methods=["POST"])
def jasenet_luo_huoltaja(huollettava_id):
    form = HenkiloTiedotAdminilleForm( request.form )

    if not form.validate() :
        return render_template("jasenet/uusi.html", form = form)

    huollettava = Henkilo.query.get(huollettava_id)
    henkilo = Henkilo()
    form.tallenna( henkilo )
    db.session.add(henkilo)
    huollettava.huoltajat.append(henkilo)
    db.session.commit()

    return redirect( url_for("jasenet_huoltajat", henkilo_id=huollettava_id))

@app.route("/jasenet/poistahuoltajuus", methods=["POST"])
def jasenet_poista_huoltajuus():
    huoltaja = Henkilo.query.get( request.form.get("huoltaja") )
    lapsi = Henkilo.query.get( request.form.get("huollettava"))
    lapsi.huoltajat.remove(huoltaja)
    db.session.commit()
    if( request.form.get("seuraava") == "huoltaja") :
        seuraavaid = huoltaja.id
    else:
        seuraavaid = lapsi.id
    return redirect( url_for("jasenet_huoltajat", henkilo_id=seuraavaid ) )


@app.route("/jasenet/<henkilo_id>/poista", methods=["POST"])
def jasenet_poista(henkilo_id):
    henkilo = Henkilo.query.get( henkilo_id )
    flash( henkilo.etunimi + " " + henkilo.sukunimi + " poistettu", "danger")
    db.session.delete(henkilo)
    db.session.commit()
    return redirect( url_for("jasenet_index") )