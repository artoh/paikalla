from application import app, db, admin_required
from flask import render_template, request, url_for, redirect, flash
from application.models import Henkilo
from application.forms.jasenet import HenkiloTiedotAdminilleForm, HenkiloTiedotForm
from datetime import datetime
from sqlalchemy.exc import IntegrityError

@app.route("/jasenet/")
@admin_required()
def jasenet_index() :
    """Henkilöiden luettelon näyttäminen"""
    if( "jasen" in request.args.keys()) :
        return render_template("jasenet/lista.html", jasenet = Henkilo.query.filter(Henkilo.jasenyysalkoi.isnot(None)).filter(Henkilo.jasenyyspaattyi == None).order_by(Henkilo.sukunimi, Henkilo.etunimi)  )
    elif( "eijasen" in request.args.keys()) :
        return render_template("jasenet/lista.html", jasenet=Henkilo.query.filter((Henkilo.jasenyysalkoi == None) | (Henkilo.jasenyyspaattyi.isnot(None))).order_by(Henkilo.sukunimi, Henkilo.etunimi))
    else:
        return render_template("jasenet/lista.html", jasenet=Henkilo.query.order_by(Henkilo.sukunimi, Henkilo.etunimi))


@app.route("/jasenet/uusi")
@admin_required()
def jasenet_uusi() :
    """Uuden henkilön luontilomake"""
    form = HenkiloTiedotAdminilleForm()
    form.jasenyysAlkoi.data = datetime.now()
    return render_template("jasenet/uusi.html", form = form)


@app.route("/jasenet", methods=["POST"])
@admin_required()
def jasenet_luo() :
    """Uuden jäsenen luominen"""
    form = HenkiloTiedotAdminilleForm( request.form )

    if not form.validate():
        flash("Ole hyvä ja tarkista syöttämäsi tiedot", "danger")
        return render_template("jasenet/uusi.html", form = form)

    henkilo = Henkilo()

    form.tallenna( henkilo )

    try:
        db.session.add(henkilo)
        db.session.commit()
    except IntegrityError:
        flash("Sähköpostiosoite on jo käytössä", "danger")
        form.email.errors.append("Sähköpostiosoite on jo käytössä");
        return render_template("jasenet/uusi.html", form=form)

    flash("Henkilö {} {} lisätty ".format(henkilo.etunimi, henkilo.sukunimi), "success")

    if henkilo.aikuinen():
        return redirect( url_for("jasenet_huollettavat", henkilo_id=henkilo.id))
    else:
        return redirect(url_for("jasenet_huoltajat", henkilo_id=henkilo.id))


@app.route("/jasenet/<henkilo_id>/tiedot/")
@admin_required()
def jasenet_tiedot(henkilo_id: int):
    """Henkilön tietojen näyttäminen"""
    henkilo = Henkilo.query.get(henkilo_id)
    form = HenkiloTiedotAdminilleForm()
    form.lataa(henkilo)

    return render_template("jasenet/tiedot.html", jasen=henkilo, form=form )


@app.route("/jasenet/<henkilo_id>/tiedot", methods=["POST"])
@admin_required()
def jasenet_paivita(henkilo_id: int):
    """Henkilön tiedon muokkausten tallentaminen"""
    form = HenkiloTiedotAdminilleForm( request.form)
    henkilo = Henkilo.query.get(henkilo_id)

    if not form.validate():
        flash("Ole hyvä ja tarkista syöttämäsi tiedot", "danger")
        return render_template("jasenet/tiedot.html", jasen=henkilo, form=form)

    form.tallenna(henkilo)
    try:
        db.session.commit()
    except IntegrityError:
        flash("Sähköpostiosoite on jo käytössä", "danger")
        form.email.errors.append("Sähköpostiosoite on jo käytössä");
        return render_template("jasenet/tiedot.html", jasen=henkilo, form=form)


    flash("Henkilön {} {} tiedot tallennettu".format(henkilo.etunimi, henkilo.sukunimi), "success")
    return redirect( url_for("jasenet_tiedot", henkilo_id=henkilo_id) )


@app.route("/jasenet/<henkilo_id>/poista", methods=["POST"])
@admin_required()
def jasenet_poista(henkilo_id: int):
    """Henkilön poistaminen tietokannasta"""
    henkilo = Henkilo.query.get( henkilo_id )
    flash( henkilo.etunimi + " " + henkilo.sukunimi + " poistettu", "danger")
    db.session.delete(henkilo)
    db.session.commit()
    return redirect( url_for("jasenet_index") )


@app.route("/jasenet/<henkilo_id>/salasana", methods=["POST"])
@admin_required()
def jasenet_salasana(henkilo_id: int):
    """Henkilön sanansana vaihtaminen ylläpidon toimin"""
    henkilo = Henkilo.query.get( henkilo_id )
    henkilo.asetaSalasana( request.form.get("salasana"))
    flash("{} {} salasana vaihdettu".format(henkilo.etunimi, henkilo.sukunimi), "info")
    db.session.commit()
    return redirect( url_for("jasenet_tiedot", henkilo_id=henkilo_id) )
