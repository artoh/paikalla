from application import db
from .ryhmassa import Ryhmassa
from .henkilo import Henkilo, ika
from sqlalchemy.sql import text
from dateutil.parser import parse
from .kokous import Kokous
from datetime import datetime

class Ryhma(db.Model):
    __tablename__ = "Ryhma"
    id = db.Column(db.Integer, primary_key=True)
    nimi = db.Column( db.String(128), nullable=False)
    paikkoja = db.Column( db.Integer, default=0)
    ilmoittautuminenAlkaa = db.Column( db.Date, nullable=True)
    ilmoittautuminenPaattyy = db.Column( db.Date, nullable=True)
    ikavahintaan = db.Column( db.Integer, default=0);
    ikaenintaan = db.Column( db.Integer, default=999);
    kuvaus = db.Column(db.Text, nullable = True)
    paattynyt = db.Column( db.Boolean, default=False)
    jasenyydet = db.relationship('Ryhmassa',lazy=True)

    def jasenet(self):
        stmt = text("SELECT ryhmassa.id, ohjaaja, sukunimi, etunimi, varotieto, Henkilo.id, syntymaaika  "
                    "FROM Ryhmassa JOIN Henkilo ON Ryhmassa.henkiloId=Henkilo.Id "
                    "WHERE Ryhmassa.ryhmaId=:ryhmaId AND Ryhmassa.paattyen IS NULL "
                    "ORDER BY sukunimi, etunimi").params(ryhmaId=self.id)
        res = db.engine.execute(stmt)
        lista = []
        for rivi in res:
            lista.append({ "ryhmassaId" : rivi[0],
                            "ohjaaja": rivi[1],
                            "sukunimi" : rivi[2],
                            "etunimi" : rivi[3],
                            "varotieto" : rivi[4],
                            "henkiloId" : rivi[5],
                            "ika": ika( parse(rivi[6]) )} )
        return lista

    def menneetKokoukset(self):
        stmt = text("SELECT Kokous.id, Kokous.alkaa, Kokous.sijainti, Kokous.kuvaus, l.lkm FROM Kokous"
                    " LEFT OUTER JOIN "
                    "( SELECT kokous, count(kokous) as lkm FROM Lasnaolo GROUP BY kokous) AS l "
                    "ON l.kokous=kokous.id WHERE Ryhmaid=:ryhmaId AND kokous.alkaa < CURRENT_TIMESTAMP "
                    ).params(ryhmaId=self.id)
        res = db.engine.execute(stmt)
        lista = []
        for rivi in res:
            lista.append({ "id" : rivi[0],
                            "alkaa": parse(rivi[1]),
                            "sijainti" : rivi[2],
                            "kuvaus" : rivi[3],
                            "lasna" : rivi[4]})
        return lista

    def seuraavaKokous(self):
        return Kokous.query.filter(Kokous.ryhmaId == self.id).filter(Kokous.paattyy > datetime.today()).order_by("alkaa").first()

    def tulevatkokoukset(self):
        stmt = text("SELECT Kokous.id, Kokous.alkaa, Kokous.paattyy, Kokous.sijainti, Kokous.kuvaus FROM Kokous "
                     "WHERE Ryhmaid=:ryhmaId AND kokous.paattyy > CURRENT_TIMESTAMP "
                    ).params(ryhmaId=self.id)
        res = db.engine.execute(stmt)
        lista = []
        for rivi in res:
            lista.append({ "kokousId" : rivi[0],
                            "alkaa": parse(rivi[1]),
                            "paattyy": parse(rivi[2]),
                            "sijainti" : rivi[3],
                            "kuvaus" : rivi[4]})
        return lista


    def ohjaajat(self):
        stmt=text("SELECT etunimi, sukunimi, puhelin, email FROM Ryhmassa JOIN Henkilo ON Ryhmassa.henkiloId=Henkilo.id "
                  "WHERE ryhmaid=:ryhmaid AND ohjaaja=1 ").params(ryhmaid=self.id)
        res = db.engine.execute(stmt)
        lista = []
        for rivi in res:
            lista.append({ "etunimi" : rivi[0],
                            "sukunimi": rivi[1],
                            "puhelin" : rivi[2],
                            "email" : rivi[3]})
        return lista

    def onkotilaa(self):
        stmt = text("SELECT COUNT(id) FROM Ryhmassa WHERE ryhmaid=:ryhmaid AND ohjaaja = 0 AND paattyen IS NULL ").params(ryhmaid=self.id)
        res = db.engine.execute(stmt)
        if res[0][0] :
            lkm = 0
        else:
            lkm = int( res[0][0])
        return self.paikkoja > lkm