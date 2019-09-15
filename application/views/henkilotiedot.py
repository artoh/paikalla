from application import app, db, login_manager, bcrypt
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user
from .autorisointi import kayttaja_autorisointi
from application.forms.jasenet import HenkiloTiedotForm, IkaValidator
from application.models.henkilo import Henkilo
from datetime import datetime

@app.route("/henkilotiedot")
@login_required
def henkilotiedot_index():
    return render_template("henkilotiedot/henkilotiedot.html")

@login_required
@app.route("/henkilotiedot/<henkilo_id>")
def henkilotiedot_muokkaus(henkilo_id):
    henkilo = kayttaja_autorisointi(henkilo_id)
    if not henkilo:
        return login_manager.unauthorized()
    form = HenkiloTiedotForm()
    form.lataa(henkilo)
    return render_template("henkilotiedot/muokkaatietoja.html", henkilo = henkilo, form=form )


@app.route("/henkilotiedot/<henkilo_id>", methods=["POST"])
def henkilotiedot_muokkaa(henkilo_id):
    henkilo = kayttaja_autorisointi(henkilo_id)
    if not henkilo:
        return login_manager.unauthorized()
    form = HenkiloTiedotForm(request.form)
    if not form.validate() :
        return render_template("henkilotiedot/muokkaatietoja.html", henkilo=henkilo, form=form)
    form.tallenna(henkilo)
    db.session.commit()
    return redirect(url_for("henkilotiedot_index"))


@app.route("/henkilotiedot/uusihuollettava")
def henkilotiedot_uusi_huollettava():
    if not current_user or not current_user.is_authenticated() or not current_user.aikuinen():
        return login_manager.unauthorized()
    form = HenkiloTiedotForm();
    form.syntymaaika.validators.append(IkaValidator(max=17, message="Huollettavan on oltava alaikäinen"))
    return render_template("henkilotiedot/uusihuollettava.html", form=form)


@app.route("/henkilotiedot/uusihuollettava", methods=["POST"])
def henkilotiedot_luo_huollettava():
    if not current_user or not current_user.is_authenticated() or not current_user.aikuinen():
        return login_manager.unauthorized()

    form = HenkiloTiedotForm(request.form)
    if not form.validate() :
        return render_template("henkilotiedot/uusihuollettava.html", form=form)

    lapsi = Henkilo()
    form.tallenna(lapsi)
    lapsi.jasenyysAlkoi = datetime.today()
    lapsi.huoltajat.append(current_user)
    db.session.add(lapsi)
    db.session.commit()
    return redirect(url_for("henkilotiedot_index"))


@app.route("/henkilotiedot/salasana", methods=["POST"])
def henkilotiedot_vaihda_salasana():
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

    henkilo.salasana = bcrypt.generate_password_hash(salasana)
    flash("Henkilön {} {} salasana vaihdettu".format(henkilo.etunimi, henkilo.sukunimi), "success")
    db.session.commit()
    return redirect(url_for("henkilotiedot_index"))

@app.route("/henkilotiedot/huoltaja", methods=["POST"])
def henkilotiedot_linkita_huoltaja():
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