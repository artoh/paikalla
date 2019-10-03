from application import app, db, login_manager
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_required
from application.helpers.autorisointi import kayttaja_autorisointi
from application.models.ryhma import Ryhma
from application.models.ryhmassa import Ryhmassa
from application.helpers.sivutus import Sivutus


@app.route("/ilmoittautumiset")
@login_required
def ilmoittautumiset_index():
    """Omien ja huollettavien ilmoittautumisten näyttäminen"""
    return render_template("ilmoittautumiset/ilmoittautumiset.html")


@app.route("/ilmoittautumiset/<ryhma_id>")
@login_required
def ilmoittautumiset_ryhma_tiedot(ryhma_id: int):
    """Ryhmän tietojen näyttäminen, kun ryhmän tiedot valittu ilmoittautumisten listasta.
       Ryhmästä näytetään ohjaajat yhteystietoineen ja tulevat kokoukset.
    """
    ryhma = Ryhma.query.get(ryhma_id)
    kokoukset = ryhma.tulevatkokoukset()
    sivutus = Sivutus( len(kokoukset),request.args.get("sivu", type=int, default=1), 20)
    return render_template("ilmoittautumiset/ryhma.html", ryhma=ryhma,
                           kokoukset=kokoukset[sivutus.alku():sivutus.loppu()],
                           linkit=sivutus.linkit())


@app.route("/ilmoittautumiset/uusilista/<henkilo_id>")
def ilmoittautumiset_uusi_lista(henkilo_id: int):
    """Näyttää listan ryhmistä, joihin kyseinen henkilö voi ikänsä puolesta ilmoittautua"""
    henkilo = kayttaja_autorisointi(henkilo_id)
    if not henkilo:
        return login_manager.unauthorized()
    return render_template("ilmoittautumiset/uusilista.html", henkilo=henkilo)


@app.route("/ilmoittautumiset/uusilista/<henkilo_id>/<ryhma_id>")
def ilmoittautumiset_uusi_tiedot(henkilo_id: int, ryhma_id: int):
    """Näyttää tarkemmat tiedot ryhmästä, josta henkilö on kiinnostunut, ja napin jolla
       pääsee ilmoittautumaan ryhmään"""
    henkilo = kayttaja_autorisointi(henkilo_id)
    if not henkilo:
        return login_manager.unauthorized()
    ryhma = Ryhma.query.get(ryhma_id)
    kokoukset = ryhma.tulevatkokoukset()
    sivutus = Sivutus( len(kokoukset),request.args.get("sivu", type=int, default=1), 20)
    return render_template("ilmoittautumiset/ryhma.html", henkilo=henkilo, ryhma=ryhma,
                           kokoukset=kokoukset[sivutus.alku():sivutus.loppu()],
                           linkit=sivutus.linkit())


@app.route("/ilmoittautumiset/ilmoittaudu", methods=["POST"])
def ilmoittautumiset_ilmoittaudu():
    """Lisää ilmoittautumisen tietokantaan.

      Kaikki argumentit välitetään lomakkeen kentissä.
    """
    henkilo = kayttaja_autorisointi(request.form.get("henkilo_id"))
    if not henkilo:
        return login_manager.unauthorized()
    ryhma = Ryhma.query.get(request.form.get("ryhma_id"))
    if not ryhma.paikkoja :
        flash("Ryhmä on valitettavasti jo täynnä, eikä ilmoittautumistasi voi hyväksyä", "danger")
        return redirect( url_for("ilmoittautumiset_index"))

    ryhmassa = Ryhmassa(ryhma.id, henkilo.id, False)
    db.session.add(ryhmassa)
    db.session.commit()
    flash("{}, tervetuloa ryhmään {}".format( henkilo.etunimi, ryhma.nimi ), "success")
    return redirect( url_for("ilmoittautumiset_index"))