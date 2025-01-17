from application import app, db, admin_required
from flask import render_template, request, url_for, redirect, flash
from application.models import Henkilo
from application.forms.jasenet import HenkiloTiedotAdminilleForm
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.exc import IntegrityError


@app.route("/jasenet/<henkilo_id>/huoltajat")
@admin_required()
def jasenet_huoltajat(henkilo_id: int):
    """Jäsentietojen hallinnassa alaikäisen jäsenen tietojen väliehti huoltajien tiedoille"""
    henkilo = Henkilo.query.get(henkilo_id)
    aikuisetsyntyneet = datetime.today() - relativedelta(years=18)
    kaikkiaikuiset = Henkilo.query.filter(Henkilo.syntymaaika < aikuisetsyntyneet ).order_by(Henkilo.sukunimi)
    aikuiset = []
    for aikuinen in kaikkiaikuiset:
        if aikuinen not in henkilo.huoltajat:
            aikuiset.append(aikuinen)

    return render_template("jasenet/huoltajat.html", jasen=henkilo, aikuiset=aikuiset)


@app.route("/jasenet/<henkilo_id>/linkitahuoltaja", methods=["POST"])
@admin_required()
def jasenet_linkita_huoltaja(henkilo_id: int):
    """Linkittää olemassa olevan henkilön muokattavana olevan henkilön huoltajaksi"""
    henkilo = Henkilo.query.get(henkilo_id)
    huoltaja = Henkilo.query.get( request.form.get("linkita") )
    henkilo.huoltajat.append(huoltaja)
    db.session.commit()
    return redirect(  url_for("jasenet_huoltajat", henkilo_id=henkilo_id))


@app.route("/jasenet/<huollettava_id>/uusihuoltaja")
@admin_required()
def jasenet_uusi_huoltaja(huollettava_id: int):
    """Uuden henkilön luominen muokattavana olevan henkilön huoltajaksi: lomakkeen näyttäminen"""
    huollettava = Henkilo.query.get(huollettava_id)
    form = HenkiloTiedotAdminilleForm()
    form.jasenyysAlkoi.data = datetime.today()
    form.aikuinen.data = True
    return render_template("jasenet/uusihuoltaja.html", henkilo=huollettava, form=form)


@app.route("/jasenet/<huollettava_id>/huoltajat", methods=["POST"])
@admin_required()
def jasenet_luo_huoltaja(huollettava_id :int):
    """Uuden henkilön luominen muokattavana olevan henkilön huoltajaksi: tietojen tallentaminen"""
    form = HenkiloTiedotAdminilleForm( request.form )

    if not form.validate() :
        flash("Ole hyvä ja tarkista syöttämäsi tiedot", "danger")
        return render_template("jasenet/uusihuoltaja.html", henkilo=huollettava, form=form)

    huollettava = Henkilo.query.get(huollettava_id)
    henkilo = Henkilo()
    form.tallenna( henkilo )

    try:
        db.session.add(henkilo)
        huollettava.huoltajat.append(henkilo)
        db.session.commit()
    except IntegrityError:
        flash("Sähköpostiosoite on jo käytössä", "danger")
        form.email.errors.append("Sähköpostiosoite on jo käytössä");
        return render_template("jasenet/uusihuoltaja.html", henkilo=huollettava, form=form)

    return redirect( url_for("jasenet_huoltajat", henkilo_id=huollettava_id))


@app.route("/jasenet/poistahuoltajuus", methods=["POST"])
@admin_required()
def jasenet_poista_huoltajuus():
    """Huoltajuuden poistaminen

      Käytetään sekä huoltajan että huollettavan lomakkeelta, joten seuraava-kenttä määrittelee,
      minne tämän lomakkeen jälkeen jatketaan."""
    huoltaja = Henkilo.query.get( request.form.get("huoltaja") )
    lapsi = Henkilo.query.get( request.form.get("huollettava"))
    lapsi.huoltajat.remove(huoltaja)
    db.session.commit()
    if( request.form.get("seuraava") == "huoltaja") :
        seuraavaid = huoltaja.id
    else:
        seuraavaid = lapsi.id
    return redirect( url_for("jasenet_huoltajat", henkilo_id=seuraavaid ) )
