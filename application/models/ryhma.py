from application import db
from .ryhmassa import Ryhmassa
from .henkilo import Henkilo, ika
from sqlalchemy.sql import text
from dateutil.parser import parse
from .kokous import Kokous
from datetime import datetime


# Postgresql-yhteensopivuuden kääreeksi
# Koska sqlite palauttaa merkkijonon ja postgre päivämäärän,
# pareseoidaan vain päivämäärät
def parsedate(pvm):
    if isinstance(pvm,str):
        return parse(pvm)
    return pvm

class Ryhma(db.Model):
    __tablename__ = "ryhma"
    id = db.Column(db.Integer, primary_key=True)
    nimi = db.Column( db.String(128), nullable=False, index=True)
    paikkoja = db.Column( db.Integer, default=0, index=True)
    ilmoittautuminenalkaa = db.Column(db.Date, nullable=True, index=True)
    ilmoittautuminenpaattyy = db.Column(db.Date, nullable=True, index=True)
    ikavahintaan = db.Column( db.Integer, default=0, index=True);
    ikaenintaan = db.Column( db.Integer, default=999, index=True);
    kuvaus = db.Column(db.Text, nullable = True)
    paattynyt = db.Column( db.Boolean, default=False, index=True)
    jasenyydet = db.relationship('Ryhmassa',lazy=True)

    def jasenet(self):
        stmt = text("SELECT ryhmassa.id, ohjaaja, sukunimi, etunimi, varotieto, Henkilo.id, syntymaaika  "
                    "FROM ryhmassa JOIN henkilo ON ryhmassa.henkiloId=henkilo.Id "
                    "WHERE ryhmassa.ryhmaid=:ryhmaid AND ryhmassa.paattyen IS NULL "
                    "ORDER BY sukunimi, etunimi").params(ryhmaid=self.id)
        res = db.engine.execute(stmt)
        lista = []
        for rivi in res:
            lista.append({ "ryhmassaId" : rivi[0],
                            "ohjaaja": rivi[1],
                            "sukunimi" : rivi[2],
                            "etunimi" : rivi[3],
                            "varotieto" : rivi[4],
                            "henkiloId" : rivi[5],
                            "ika": ika(rivi[6])})
        return lista

    def menneetKokoukset(self):
        stmt = text("SELECT kokous.id, kokous.alkaa, kokous.sijainti, kokous.kuvaus, l.lkm FROM kokous"
                    " LEFT OUTER JOIN "
                    "( SELECT kokous, count(kokous) as lkm FROM lasnaolo GROUP BY kokous) AS l "
                    "ON l.kokous=kokous.id WHERE ryhmaid=:ryhmaid AND kokous.alkaa < CURRENT_TIMESTAMP "
                    ).params(ryhmaid=self.id)
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
        return Kokous.query.filter(Kokous.ryhmaid == self.id).filter(Kokous.paattyy > datetime.today()).order_by("alkaa").first()

    def tulevatkokoukset(self):
        stmt = text("SELECT kokous.id, kokous.alkaa, kokous.paattyy, kokous.sijainti, kokous.kuvaus FROM kokous "
                     "WHERE ryhmaid=:ryhmaid AND kokous.paattyy > CURRENT_TIMESTAMP "
                    ).params(ryhmaid=self.id)
        res = db.engine.execute(stmt)
        lista = []
        for rivi in res:
            lista.append({ "kokousId" : rivi[0],
                            "alkaa": parsedate(rivi[1]),
                            "paattyy": parsedate(rivi[2]),
                            "sijainti" : rivi[3],
                            "kuvaus" : rivi[4]})
        return lista


    def ohjaajat(self):
        stmt=text("SELECT etunimi, sukunimi, puhelin, email FROM ryhmassa JOIN henkilo ON ryhmassa.henkiloid=henkilo.id "
                  "WHERE ryhmaid=:ryhmaid AND ohjaaja ").params(ryhmaid=self.id)
        res = db.engine.execute(stmt)
        lista = []
        for rivi in res:
            lista.append({ "etunimi" : rivi[0],
                            "sukunimi": rivi[1],
                            "puhelin" : rivi[2],
                            "email" : rivi[3]})
        return lista

    def onkotilaa(self):
        stmt = text("SELECT COUNT(id) FROM ryhmassa WHERE ryhmaid=:ryhmaid AND not ohjaaja AND paattyen IS NULL ").params(ryhmaid=self.id)
        res = db.engine.execute(stmt)
        if res[0][0] :
            lkm = 0
        else:
            lkm = int( res[0][0])
        return self.paikkoja > lkm
