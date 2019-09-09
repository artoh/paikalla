from application import db


class Ryhmassa(db.Model):
    __tablename__ = "Ryhmassa"
    id = db.Column(db.Integer, primary_key=True)
    ryhma = db.Column(db.Integer, db.ForeignKey('Ryhma.id'), nullable=False)
    jasen = db.Column(db.Integer, db.ForeignKey('Henkilo.id'), nullable=False)
    ohjaaja = db.Column(db.Boolean, default=False)
    alkaen = db.Column(db.Date, nullable=False)
    paattyen = db.Column( db.Date, nullable=True)
