from application import db
from datetime import datetime

class Ryhmassa(db.Model):
    __tablename__ = "ryhmassa"
    id = db.Column(db.Integer, primary_key=True)
    ryhmaid = db.Column(db.Integer, db.ForeignKey('ryhma.id', ondelete="CASCADE"), nullable=False)
    henkiloid = db.Column(db.Integer, db.ForeignKey('henkilo.id', ondelete="CASCADE"), nullable=False)
    ohjaaja = db.Column(db.Boolean, default=False)
    alkaen = db.Column(db.Date, nullable=False)
    paattyen = db.Column( db.Date, nullable=True)
    jasen = db.relationship('Henkilo', lazy=True)
    ryhma = db.relationship('Ryhma', lazy=True)

    def __init__(self, ryhmaId, jasenId, ohjaaja = False):
        self.ryhmaid = ryhmaId
        self.henkiloid = jasenId
        self.ohjaaja = ohjaaja
        self.alkaen = datetime.today()
