from application import app, db, login_manager
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_required
from .autorisointi import kayttaja_autorisointi
from application.models.ryhma import Ryhma
from application.models.ryhmassa import Ryhmassa


@app.route("/ilmoittautumiset")
@login_required
def ilmoittautumiset_index():
    return render_template("ilmoittautumiset/ilmoittautumiset.html")


@app.route("/ilmoittautumiset/<ryhma_id>")
@login_required
def ilmoittautumiset_ryhma_tiedot(ryhma_id):
    ryhma = Ryhma.query.get(ryhma_id)
    return render_template("ilmoittautumiset/ryhma.html", ryhma=ryhma)


@app.route("/ilmoittautumiset/uusilista/<henkilo_id>")
def ilmoittautumiset_uusi_lista(henkilo_id):
    henkilo = kayttaja_autorisointi(henkilo_id)
    if not henkilo:
        return login_manager.unauthorized()
    return render_template("ilmoittautumiset/uusilista.html", henkilo=henkilo)


@app.route("/ilmoittautumiset/uusilista/<henkilo_id>/<ryhma_id>")
def ilmoittautumiset_uusi_tiedot(henkilo_id, ryhma_id):
    henkilo = kayttaja_autorisointi(henkilo_id)
    if not henkilo:
        return login_manager.unauthorized()
    ryhma = Ryhma.query.get(ryhma_id)
    return render_template("ilmoittautumiset/ryhma.html", henkilo=henkilo, ryhma=ryhma)

@app.route("/ilmoittautumiset/ilmoittaudu", methods=["POST"])
def ilmoittautumiset_ilmoittaudu():
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