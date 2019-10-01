from application import app, db, login_manager, bcrypt
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user
from .autorisointi import kayttaja_autorisointi
from application.forms.jasenet import HenkiloTiedotForm, HenkiloTiedotLapsiForm
from application.models.henkilo import Henkilo
from datetime import datetime
from sqlalchemy.exc import IntegrityError

@app.route("/henkilotiedot")
@login_required
def henkilotiedot_index():
    """Omien ja huollettavien henkilötietojen näyttäminen"""
    return render_template("henkilotiedot/henkilotiedot.html")


@login_required
@app.route("/henkilotiedot/<henkilo_id>")
def henkilotiedot_muokkaus(henkilo_id: int):
    """Omien tai huollettavan henkilötietojen muokkausnäkymän näyttäminen"""
    henkilo = kayttaja_autorisointi(henkilo_id)
    if not henkilo:
        return login_manager.unauthorized()
    form = HenkiloTiedotForm()
    form.lataa(henkilo)
    return render_template("henkilotiedot/muokkaatietoja.html", henkilo = henkilo, form=form )


@app.route("/henkilotiedot/<henkilo_id>", methods=["POST"])
def henkilotiedot_muokkaa(henkilo_id):
    """Omien tai huollettavan henkilötietojen muokkauksien tallentaminen"""
    henkilo = kayttaja_autorisointi(henkilo_id)
    if not henkilo:
        return login_manager.unauthorized()
    form = HenkiloTiedotForm(request.form)
    if not form.validate() :
        flash("Ole hyvä ja tarkista syöttämäsi tiedot", "danger")
        return render_template("henkilotiedot/muokkaatietoja.html", henkilo=henkilo, form=form)
    form.tallenna(henkilo)

    try:
        db.session.commit()
    except IntegrityError:
        flash("Sähköpostiosoite on jo käytössä", "danger")
        form.email.errors.append("Sähköpostiosoite on jo käytössä");
        return render_template("henkilotiedot/muokkaatietoja.html", henkilo=henkilo, form=form)

    return redirect(url_for("henkilotiedot_index"))


@app.route("/henkilotiedot/uusihuollettava")
def henkilotiedot_uusi_huollettava():
    """Uuden huollettavan itselisääminen - lomakkeen näyttäminen"""
    if not current_user or not current_user.is_authenticated() or not current_user.aikuinen():
        return login_manager.unauthorized()
    form = HenkiloTiedotLapsiForm();
    return render_template("henkilotiedot/uusihuollettava.html", form=form)


@app.route("/henkilotiedot/uusihuollettava", methods=["POST"])
def henkilotiedot_luo_huollettava():
    """Uuden huollettavan itselisääminen - tietojen tallentaminen"""

    if not current_user or not current_user.is_authenticated() or not current_user.aikuinen():
        return login_manager.unauthorized()

    form = HenkiloTiedotForm(request.form)
    if not form.validate() :
        flash("Ole hyvä ja tarkista syöttämäsi tiedot", "danger")
        return render_template("henkilotiedot/uusihuollettava.html", form=form)

    lapsi = Henkilo()
    form.tallenna(lapsi)
    lapsi.jasenyysalkoi = datetime.today()
    lapsi.huoltajat.append(current_user)
    db.session.add(lapsi)

    try:
        db.session.commit()
    except IntegrityError:
        flash("Sähköpostiosoite on jo käytössä", "danger")
        form.email.errors.append("Sähköpostiosoite on jo käytössä");
        return render_template("henkilotiedot/uusihuollettava.html", form=form);

    return redirect(url_for("henkilotiedot_index"))


@app.route("/henkilotiedot/salasana", methods=["POST"])
def henkilotiedot_vaihda_salasana():
    """Oman tai huollettavan sanasanan vaihtaminen

    Kaikki parametrit välitetään lomakkeen kentissä
    """

    salasana = request.form.get("salasana")
    if not current_user or not current_user.is_authenticated():
        return login_manager.unauthorized()

    if len(salasana) < 6 :
        # Hylätään hiljaisesti, koska javascript torppaa tämän sovelluksessa
        return redirect(url_for("henkilotiedot_index"))

    henkiloid = int(request.form.get("henkiloid"))
    print(" -  henkilöid {}  nykyinen {}".format(henkiloid, current_user.id))
    if henkiloid == current_user.id:
        henkilo = Henkilo.query.get(current_user.id)  # Oman salasanan saa vaihtaa
        print(" --- haettu {}".format(henkilo.id))
    else:
        # Tarkistetaan, että ollaan vaihtamassa huollettavan salasanaa
        henkilo = kayttaja_autorisointi(henkiloid)
        if not henkilo:
            return login_manager.unauthorized()

    henkilo.asetaSalasana(salasana)
    flash("Henkilön {} {} salasana vaihdettu".format(henkilo.etunimi, henkilo.sukunimi), "success")
    db.session.commit()
    return redirect(url_for("henkilotiedot_index"))


@app.route("/henkilotiedot/huoltaja", methods=["POST"])
def henkilotiedot_linkita_huoltaja():
    """Olemassaolevan henkilön lisääminen huoltajaksi itsensä lisäksi

    Tarvittavat parametrit välitetään lomakkeen kentissä.
    """

    lapsi = kayttaja_autorisointi( request.form.get("lapsiid") )
    if not lapsi:
        return login_manager.unauthorized()
    huoltajaemail = request.form.get("huoltaja")
    huoltaja = Henkilo.query.filter(Henkilo.email == huoltajaemail).first()

    if not huoltaja or not huoltaja.aikuinen():
        return render_template("henkilotiedot/henkilotiedot.html",
                               huoltajavirhe={"lapsi":lapsi, "huoltaja":huoltajaemail, "virhe":"Sähköpostiosoitteella ei löydy aikuista."})

    for huollettava in huoltaja.huollettavat :
        if huollettava.id == lapsi.id :
            return render_template("henkilotiedot/henkilotiedot.html",
                                   huoltajavirhe={"lapsi": lapsi, "huoltaja": huoltajaemail,
                                                  "virhe": "On jo lapsen huoltaja."})

    # Voidaan linkittää huoltajaksi
    lapsi.huoltajat.append(huoltaja)
    flash("{} {} lisättiin huoltajaksi".format(huoltaja.etunimi, huoltaja.sukunimi), "success")
    db.session.commit()
    return redirect(url_for("henkilotiedot_index"))
