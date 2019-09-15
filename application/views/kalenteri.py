from application import app
from flask import render_template
from flask_login import login_required, current_user

@app.template_filter('kpvm')
def format_date(value):
    return value.strftime("%A %d.%m.%Y")

@login_required
@app.route("/kalenteri")
def kalenteri():
    return render_template("kalenteri/kalenteri.html", kalenteri=current_user.kalenteri())