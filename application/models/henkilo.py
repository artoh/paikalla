from application import db

class Henkilo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    etunimi = db.Column( db.String(128), nullable=False)
    sukunimi = db.Column( db.String(128), nullable=False)
    puhelin = db.Column( db.String(32), nullable=True)
    email = db.column( db.String(64), nullable=True)
    