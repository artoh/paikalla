from application import db


Lasnaolo = db.Table('Lasnaolo',
    db.Column('ryhmassa', db.Integer, db.ForeignKey('Ryhmassa.id'), primary_key=True),
    db.Column('kokous', db.Integer, db.ForeignKey('Kokous.id'), primary_key=True) )


class Kokous(db.Model) :
    __tablename__ = "Kokous"
    id = db.Column(db.Integer, primary_key=True)
    ryhma = db.Column( db.Integer, db.ForeignKey('Ryhma.id'), nullable=False)
    alkaa = db.Column( db.DateTime, nullable=False )
    paattyy = db.Column( db.DateTime, nullable=True)
    sijainti = db.Column( db.Text, nullable=True)
    kuvaus = db.Column( db.Text, nullable=True)
    memo = db.Column( db.Text, nullable=True)
    lasna = db.relationship('Ryhmassa', secondary=Lasnaolo, lazy=True,
                            backref=db.backref('kokokukset', lazy=True))

