from application import app, db
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_required

@app.route("/ilmoittautumiset")
@login_required
def ilmoittautumiset_index():
    return render_template("mina/ilmoittautumiset.html")
