from application import db


class Ryhmassa(db.Model):
    __tablename__ = "Ryhmassa"
    id = db.Column(db.Integer, primary_key=True)
    ryhmaId = db.Column(db.Integer, db.ForeignKey('Ryhma.id', ondelete="CASCADE"), nullable=False)
    henkiloId = db.Column(db.Integer, db.ForeignKey('Henkilo.id', ondelete="CASCADE"), nullable=False)
    ohjaaja = db.Column(db.Boolean, default=False)
    alkaen = db.Column(db.Date, nullable=False)
    paattyen = db.Column( db.Date, nullable=True)
    jasen = db.relationship('Henkilo', lazy=True)
    ryhma = db.relationship('Ryhma', lazy=True)

    def __init__(self, ryhmaId, jasenId, ohjaaja = False):
        self.ryhmaId = ryhmaId
        self.henkiloId = jasenId
        self.ohjaaja = ohjaaja