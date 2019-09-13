from application import app, db
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_required

@app.route("/henkilotiedot")
@login_required
def henkilotiedot_index():
    return render_template("mina/henkilotiedot.html")

