from application import app
from flask import render_template, request
from flask_login import login_required, current_user
from .sivutus import Sivutus
from datetime import datetime

@app.template_filter('kpvm')
def format_date(value):
    """Kalenterin käyttämä filtteri päivämäärän näyttämiseksi niin, että mukana on myös viikonpäivä"""
    return value.strftime("%A %d.%m.%Y")

@login_required
@app.route("/kalenteri")
def kalenteri():
    """Näyttää kalenterin, jossa nykyisen käyttäjän ja hänen huollettaviensa tulevat kokoukset"""
    kalenteri = current_user.kalenteri()
    sivutus = Sivutus( len(kalenteri), request.args.get("sivu", type=int, default=1) )

    return render_template("kalenteri/kalenteri.html", kalenteri=kalenteri[ sivutus.alku() : sivutus.loppu()], linkit=sivutus.linkit(),
                           tanaan=datetime.today().date())