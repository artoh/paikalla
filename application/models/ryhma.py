from application import db


class Ryhma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nimi = db.Column( db.String(128), nullable=False)
    paikkoja = db.Column( db.Integer, default=0)
    ilmoittautuminenAlkaa = db.Column( db.DateTime, nullable=True)
    ilmoittautuminenPaattyy = db.Column( db.DateTime, nullable=True)
    kuvaus = db.Column(db.Text, nullable = True)
