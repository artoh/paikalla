from application import db
from .henkilo import Henkilo, ika
from sqlalchemy.sql import text
from dateutil.parser import parse
from .kokous import Kokous
from datetime import datetime, timedelta

from application.models import parsedate


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
                            "ika": ika(parsedate(rivi[6]))})
        return lista

    def menneetKokoukset(self):
        aika = datetime.now() - timedelta( minutes=30)
        stmt = text("SELECT kokous.id, kokous.alkaa, kokous.sijainti, kokous.kuvaus, l.lkm FROM kokous"
                    " LEFT OUTER JOIN "
                    "( SELECT kokous, count(kokous) as lkm FROM lasnaolo GROUP BY kokous) AS l "
                    "ON l.kokous=kokous.id WHERE ryhmaid=:ryhmaid AND kokous.alkaa < :aika "
                    ).params(ryhmaid=self.id, aika=aika )
                    # Ajan vertailu tehdään datetime-funktioilla eikä SQL:n aikafunktioilla, jotta
                    # palvelimen aikavyöhyke ei vaikuttaisi vertailuun.
        res = db.engine.execute(stmt)
        lista = []
        for rivi in res:
            lista.append({ "id" : rivi[0],
                            "alkaa": parsedate(rivi[1]),
                            "sijainti" : rivi[2],
                            "kuvaus" : rivi[3],
                            "lasna" : rivi[4]})
        return lista

    def seuraavaKokous(self):
        return Kokous.query.filter(Kokous.ryhmaid == self.id).filter(Kokous.paattyy > datetime.today()).order_by("alkaa").first()

    def tulevatkokoukset(self):
        aika = datetime.now()
        stmt = text("SELECT kokous.id, kokous.alkaa, kokous.paattyy, kokous.sijainti, kokous.kuvaus FROM kokous "
                     "WHERE ryhmaid=:ryhmaid AND kokous.paattyy > :aika"
                    ).params(ryhmaid=self.id, aika=aika)
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

    KAIKKIRYHMAT = 0
    AKTIIVISETRYHMAT = 1
    PAATTYNEETRYHMAT = 2

    @staticmethod
    def lista(paattymissuodatin):
        if paattymissuodatin == Ryhma.AKTIIVISETRYHMAT:
            ehto = "WHERE NOT paattynyt"
        elif paattymissuodatin == Ryhma.PAATTYNEETRYHMAT:
            ehto = "WHERE paattynyt"
        else:
            ehto = ""

        stmt = text("SELECT ryhma.id, ryhma.nimi, ryhma.ikavahintaan, ryhma.ikaenintaan, ryhma.ilmoittautuminenalkaa, ryhma.ilmoittautuminenpaattyy, "
                    "ryhma.paikkoja, a.lkm "            
                    "FROM ryhma LEFT OUTER JOIN "
                    "(SELECT ryhmaid, count(id) as lkm FROM ryhmassa WHERE NOT ohjaaja AND paattyen IS NULL GROUP BY ryhmaid) "
                    "AS a ON ryhma.id=a.ryhmaid " + ehto + " ORDER BY ryhma.nimi")

        res = db.engine.execute(stmt)
        lista = []

        for rivi in res:
            lista.append({"id" : rivi[0],
                          "nimi": rivi[1],
                          "ikavahintaan": rivi[2],
                          "ikaenintaan": rivi[3],
                          "ilmoittautuminenalkaa": parsedate(rivi[4]),
                          "ilmoittautuminenpaattyy": parsedate(rivi[5]),
                          "paikkoja": rivi[6],
                          "ilmoittautuneita" : rivi[7]})
        return lista