from application import db

Huoltajuus = db.Table('Huoltajuus',
      db.Column( 'huoltaja', db.Integer, db.ForeignKey('Henkilo.id'), primary_key=True),
      db.Column( 'huollettava', db.Integer, db.ForeignKey('Henkilo.id'), primary_key=True))


class Henkilo(db.Model):
    __tablename__ = "Henkilo"
    id = db.Column(db.Integer, primary_key=True)
    etunimi = db.Column( db.String(128), nullable=False)
    sukunimi = db.Column( db.String(128), nullable=False)
    puhelin = db.Column( db.String(32), nullable=True)
    email = db.Column( db.String(64), nullable=True)
    salasana = db.Column( db.Text, nullable=True)
    aikuinen = db.Column( db.Boolean, default=False)
    toimihenkilo = db.Column( db.Boolean, default=False )
    varotieto = db.Column (db.Text, nullable=True)
    jasenyysAlkoi = db.Column( db.Date, nullable=True)
    jasenyysPaattyi = db.Column( db.Date, nullable=True)
    huoltajat = db.relationship('Henkilo',
                            secondary=Huoltajuus,
                            primaryjoin=id == Huoltajuus.c.huollettava,
                            secondaryjoin=id == Huoltajuus.c.huoltaja,
                            backref=db.backref('huollettavat'))
