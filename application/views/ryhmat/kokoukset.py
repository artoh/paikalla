from application import app, db
from flask import render_template, request, url_for, redirect, flash
from application.models import Ryhma, Ryhmassa, Henkilo
from datetime import datetime, timedelta
from application.forms.kokoukset import KokousTiedotForm, KokousSarjaForm
from application.models import Kokous
from application.models.kokous import Lasnaolo

@app.route("/ryhmat/<ryhma_id>/kokoukset")
def ryhmat_kokoukset(ryhma_id):
    ryhma = Ryhma.query.get(ryhma_id)
    kokoukset = Kokous.query.filter(Kokous.ryhmaid == ryhma.id, Kokous.paattyy > datetime.now()).order_by("alkaa")
    return render_template("ryhmat/kokoukset.html", ryhma=ryhma, kokoukset=kokoukset)

@app.route("/ryhmat/<ryhma_id>/kokoukset/uusi")
def ryhmat_kokoukset_uusi(ryhma_id):
    ryhma = Ryhma.query.get(ryhma_id)
    form = KokousTiedotForm()
    return render_template("ryhmat/uusikokous.html", ryhma=ryhma, form=form)

@app.route("/ryhmat/<ryhma_id>/kokoukset/", methods=["POST"])
def ryhmat_luo_kokous(ryhma_id):
    form = KokousTiedotForm(request.form)
    ryhma = Ryhma.query.get(ryhma_id)

    if not form.validate():
        return render_template("ryhmat/uusikokous.html", ryhma=ryhma, form=form)

    kokous = Kokous(ryhma.id)
    form.tallenna(kokous)
    db.session.add(kokous)
    db.session.commit();

    return redirect( url_for("ryhmat_kokoukset", ryhma_id=ryhma_id) )

@app.route("/ryhmat/<ryhma_id>/kokoukset/uusisarja")
def ryhmat_kokoukset_uusisarja(ryhma_id):
    ryhma = Ryhma.query.get(ryhma_id)
    form = KokousSarjaForm()
    return render_template("ryhmat/uusisarja.html", ryhma=ryhma, form=form)

@app.route("/ryhmat/<ryhma_id>/kokoussarja/", methods=["POST"])
def ryhmat_luo_kokoussarja(ryhma_id):
    form = KokousSarjaForm(request.form)
    ryhma = Ryhma.query.get(ryhma_id)

    if not form.validate():
        return render_template("ryhmat/uusisarja.html", ryhma=ryhma, form=form)

    paiva = form.alkaa.data
    kokoukset = 0
    while paiva < form.paattyy.data:
        if( paiva.weekday() == int(form.viikonpaiva.data) ) :
            kokous = Kokous(ryhma.id)
            kokous.alkaa = datetime.combine(paiva, form.alkaaklo.data)
            kokous.paattyy = datetime.combine(paiva, form.paattyyklo.data)
            kokous.sijainti = form.sijainti.data
            kokous.kuvaus = form.kuvaus.data
            db.session.add(kokous)
            kokoukset += 1

        paiva = paiva + timedelta(days=1)

    db.session.commit()
    flash("Lisätty {}  kokousta".format(kokoukset),"success")

    return redirect( url_for("ryhmat_kokoukset", ryhma_id=ryhma_id) )


@app.route("/ryhmat/poistakokous/<kokous_id>", methods=["POST"])
def ryhmat_poista_kokous(kokous_id):
    kokous = Kokous.query.get(kokous_id)
    ryhma = kokous.ryhma
    flash("Kokous {:%d.%m.%y klo %H.%M} poistettiin".format(kokous.alkaa),"danger")
    db.session.delete(kokous)
    db.session.commit()
    return redirect( url_for("ryhmat_kokoukset", ryhma_id=ryhma.id))


@app.route("/ryhmat/kokoukset/<kokous_id>")
def ryhmat_kokoukset_muokkaa(kokous_id):
    kokous = Kokous.query.get(kokous_id)

    if kokous.alkaa < datetime.today() - timedelta(minutes=15) :
        return redirect( url_for("ryhmat_menneet_muokkaa", kokous_id=kokous_id))

    form = KokousTiedotForm()
    form.lataa(kokous)
    return render_template("ryhmat/muokkaakokous.html", kokous=kokous, ryhma=kokous.ryhma, form=form)


@app.route("/ryhmat/kokoukset/<kokous_id>", methods=["POST"])
def ryhmat_muokkaa_kokous(kokous_id):
    kokous = Kokous.query.get(kokous_id)
    form = KokousTiedotForm( request.form )
    if not form.validate():
        return render_template("ryhmat/muokkaakokous.html", kokous=kokous, ryhma=kokous.ryhma, form=form)
    form.tallenna(kokous)
    db.session.commit()
    return redirect( url_for("ryhmat_kokoukset", ryhma_id=kokous.ryhma.id))


@app.route("/ryhmat/<ryhma_id>/menneet")
def ryhmat_menneet(ryhma_id):
    ryhma = Ryhma.query.get(ryhma_id)
    return render_template("ryhmat/menneet.html", ryhma=ryhma)


@app.route("/ryhmat/menneet/<kokous_id>")
def ryhmat_menneet_muokkaa(kokous_id):
    kokous = Kokous.query.get(kokous_id)
    return render_template("ryhmat/lasnalista.html", kokous=kokous, ryhma=kokous.ryhma)


@app.route("/rymat/menneet/<kokous_id>", methods=["POST"])
def ryhmat_muokkaa_mennyt(kokous_id):
    kokous = Kokous.query.get(kokous_id)
    kokous.memo = request.form.get("memo")
    kokous.lasna = []

    for key in request.form.keys():
        if key.isdigit():
            ryhmassa = Ryhmassa.query.get( int(key) )
            kokous.lasna.append(ryhmassa)

    db.session.commit()
    return redirect(url_for("ryhmat_menneet", ryhma_id=kokous.ryhmaid) )

