from application import db
from .ryhmassa import Ryhmassa
from .henkilo import Henkilo
from sqlalchemy.sql import text

class Ryhma(db.Model):
    __tablename__ = "Ryhma"
    id = db.Column(db.Integer, primary_key=True)
    nimi = db.Column( db.String(128), nullable=False)
    paikkoja = db.Column( db.Integer, default=0)
    ilmoittautuminenAlkaa = db.Column( db.DateTime, nullable=True)
    ilmoittautuminenPaattyy = db.Column( db.DateTime, nullable=True)
    kuvaus = db.Column(db.Text, nullable = True)
    paattynyt = db.Column( db.Boolean, default=False)
    jasenyydet = db.relationship('Ryhmassa',lazy=True)