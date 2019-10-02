from application import db
from .henkilo import ika
from sqlalchemy.sql import text
from .kokous import Kokous
from datetime import datetime, timedelta, date

from application.models import parsedate


class Ryhma(db.Model):
    """Ryhmän tiedot"""
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

    def jasenet(self) -> list:
        """Luettelo ryhmän nykyisistä jäsenistä ja ohjaajista"""
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

    def menneetKokoukset(self) -> list:
        """Luettelo ryhmän menneistä kokoontumisista ja läsnäolleiden määrästä"""
        aika = datetime.now() - timedelta( minutes=30)
        stmt = text("SELECT kokous.id, kokous.alkaa, kokous.sijainti, kokous.kuvaus, count(lasnaolo.ryhmassa) FROM kokous "
                    "LEFT OUTER JOIN lasnaolo on kokous.id=lasnaolo.kokous " 
                    "WHERE ryhmaid=:ryhmaid AND kokous.alkaa < :aika "
                    "GROUP BY kokous.id, kokous.alkaa, kokous.sijainti, kokous.kuvaus "
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

    def seuraavaKokous(self) -> Kokous:
        """Tämän ryhmän seuraava kokous"""
        return Kokous.query.filter(Kokous.ryhmaid == self.id).filter(Kokous.paattyy > datetime.today()).order_by("alkaa").first()

    def tulevatkokoukset(self) -> list:
        """Ryhmän tulevat kokoukset (kokoukset, jotka eivät ole vielä päättyneet"""
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


    def ohjaajat(self) -> list:
        """Lista ryhmän ohjaajista ja heidän yhteystiedoistaan"""
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

    def onkotilaa(self) -> bool:
        """Onko ryhmässä tilaa uusille ilmoittautumisille"""
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
    def lista(paattymissuodatin) -> list:
        """Luettelo kaikista ryhmista

        :param paattymissuodatin: Luetellaanko kaikki ryhmät, aktiiviset ryhmät vai päättyneet ryhmät"""
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

    @staticmethod
    def yhteistilasto(mista: date, mihin: date) -> list:
        """Yhdistyksen yleistilastoon ryhmien kokoontumistiedot"""
        stmt = text("select ryhma.nimi, kokous.ryhmaid, count(distinct kokous.id), count(lasnaolo.kokous) from kokous "
                    "left outer join lasnaolo on lasnaolo.kokous=kokous.id "
                    "join ryhma on kokous.ryhmaid=ryhma.id "
                    "where kokous.alkaa between :alkaa and :loppuu "
                    "group by kokous.ryhmaid, ryhma.nimi "
                    "order by nimi").params(alkaa = mista, loppuu=mihin)
        res = db.engine.execute(stmt)
        lista = []
        for rivi in res:
            lista.append({"nimi" : rivi[0],
                          "id": rivi[1],
                          "kokouksia" : rivi[2],
                          "lasna": rivi[3]})

        return lista

    def ryhmantilasto(self, mista: date, mihin: date) -> dict:
        """Ryhmän oma tilasto, jossa myös läsnäolotilastot """
        stmt = text("select count(distinct kokous.id), count(lasnaolo.kokous) from kokous "
                    "left outer join lasnaolo on lasnaolo.kokous=kokous.id "                    
                    "where kokous.alkaa between :alkaa and :loppuu "
                    "and kokous.ryhmaid=:ryhmaid ").params(alkaa=mista, loppuu=mihin, ryhmaid=self.id)
        res = db.engine.execute(stmt)
        tulos = {}
        for rivi in res:
            tulos["tilasto"] = {"kokouksia" : rivi[0], "lasna" : rivi[1]}

        stmt = text("select sukunimi, etunimi, count(lasnaolo.kokous) as lasna, ryhmassa.ohjaaja from lasnaolo "
                    "join ryhmassa on lasnaolo.ryhmassa=ryhmassa.id "
                    "join henkilo on ryhmassa.henkiloid=henkilo.id "
                    " join kokous on lasnaolo.kokous=kokous.id "
                    "where kokous.ryhmaid=:ryhmaid and "
                    "kokous.alkaa between :alkaa and :loppuu group by henkilo.id, ryhmassa.ohjaaja order by lasna desc"
                    ).params(alkaa=mista, loppuu=mihin, ryhmaid=self.id )
        res = db.engine.execute(stmt)
        lasnaolot = []
        for rivi in res:
            lasnaolot.append({"sukunimi":rivi[0],
                              "etunimi": rivi[1],
                              "lasna" : rivi[2],
                              "ohjaaja": rivi[3]})
        tulos["lasnaolot"]=lasnaolot
        return tulos
