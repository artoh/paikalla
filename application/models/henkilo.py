from application import db, bcrypt
from datetime import date
from sqlalchemy.sql import text
from flask_login import current_user
from datetime import datetime

from application.models import parsedate

Huoltajuus = db.Table('huoltajuus',
      db.Column( 'huoltaja', db.Integer, db.ForeignKey('henkilo.id', ondelete="CASCADE"), primary_key=True),
      db.Column( 'huollettava', db.Integer, db.ForeignKey('henkilo.id', ondelete="CASCADE"), primary_key=True))


def ika(syntymapaiva : datetime.date) -> int:
    """Ikä tänään täysinä vuosina syntymäpäivän perusteella"""
    tanaan = date.today()
    vuotta = tanaan.year - syntymapaiva.year
    if tanaan.month < syntymapaiva.month or tanaan.month == syntymapaiva.month and tanaan.day < syntymapaiva.day:
        vuotta -= 1
    return vuotta


class Henkilo(db.Model):
    """Yksittäisen henkilön (jäsen tai huoltaja) tiedot"""
    __tablename__ = "henkilo"
    id = db.Column(db.Integer, primary_key=True)
    etunimi = db.Column( db.String(128), nullable=False)
    sukunimi = db.Column( db.String(128), nullable=False, index=True)
    puhelin = db.Column( db.String(32), nullable=True)
    email = db.Column( db.String(64), nullable=True, unique=True)
    salasana = db.Column( db.Text, nullable=True)
    syntymaaika = db.Column( db.Date, nullable=False)
    toimihenkilo = db.Column( db.Boolean, default=False )
    varotieto = db.Column (db.Text, nullable=True)
    jasenyysalkoi = db.Column(db.Date, nullable=True)
    jasenyyspaattyi = db.Column(db.Date, nullable=True)
    huoltajat = db.relationship('Henkilo',
                            secondary=Huoltajuus,
                            primaryjoin=id == Huoltajuus.c.huollettava,
                            secondaryjoin=id == Huoltajuus.c.huoltaja,
                            backref=db.backref('huollettavat'),
                            lazy=True)
    ryhmat = db.relationship('Ryhmassa', backref='ryhmat', lazy=True)

    def ika(self) -> int:
        """Henkilön ikä täysinä vuosina tänään"""
        return ika(self.syntymaaika)

    def aikuinen(self) -> bool:
        """Henkilö on vähintään 18-vuotias"""
        return self.ika() >= 18

    def jasen(self) -> bool:
        """Henkilö on yhdistyksen jäsen"""
        return self.jasenyysalkoi and not self.jasenyyspaattyi

    def asetaSalasana(self, selvakielisena : str):
        """Kryptaa ja asettaa salasanan"""
        self.salasana = bcrypt.generate_password_hash(selvakielisena).decode('utf-8')

    def get_id(self) -> int:
        return self.id

    def is_active(self):
        """Käyttäjä voi kirjautua, jos sähköposti ja salasana asetettu"""
        return  len(self.email) and len( self.salasana )

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def mahdollisetryhmat(self) -> list:
        """Ryhmät, joihin voi ilmoittautua iän puolesta"""

        stmt = text("select ryhma.id,nimi,paikkoja,kuvaus,a.lkm, ikavahintaan, ikaenintaan  "
                    "from ryhma left outer join "
                    "(select ryhmaid, count(id) as lkm from ryhmassa where not ohjaaja and  paattyen is null group by ryhmaid) as a on ryhma.id=a.ryhmaid "
                    "where ilmoittautuminenalkaa <= :tanaan and ilmoittautuminenpaattyy >= :tanaan "
                    "and ikavahintaan <= :ika and ikaenintaan >= :ika "
                    "and ryhma.id not in (select ryhmaid from ryhmassa where henkiloid=:henkiloid) "
                    "and not ryhma.paattynyt "
                    "order by nimi"
                    ).params(ika=self.ika(), henkiloid=self.id, tanaan=datetime.today())

        res = db.engine.execute(stmt)
        lista = []
        for rivi in res:
            if rivi[4] :
                lkm = rivi[4]
            else:
                lkm = 0
            lista.append({"id": rivi[0],
                          "nimi":rivi[1],
                          "paikkoja":rivi[2],
                          "kuvaus":rivi[3],
                          "lkm":lkm,
                          "ikavahintaan" : rivi[5],
                          "ikaenintaan": rivi[6]})
        return lista

    def kalenteri(self) -> list:
        """Lista omista ja huollettavien tulevista kokoontumisista, päivittäin koottuna"""
        stmt = text("SELECT henkilo.etunimi, ryhma.nimi, kokous.alkaa, kokous.paattyy, kokous.sijainti, kokous.kuvaus, kokous.id, ryhmassa.ohjaaja, Henkilo.id "
                    "FROM henkilo JOIN ryhmassa ON henkilo.id=ryhmassa.henkiloid JOIN ryhma ON ryhmassa.ryhmaid=ryhma.id JOIN kokous ON kokous.ryhmaid=ryhma.id "
                    "WHERE (ryhmassa.henkiloid=:henkiloid "
                    "OR ryhmassa.henkiloid in (SELECT huollettava FROM huoltajuus WHERE huoltaja=:henkiloid)) AND kokous.paattyy >= :tanaan "
                    "ORDER BY kokous.alkaa").params(henkiloid=self.id, tanaan=datetime.today())
        res = db.engine.execute(stmt)
        paiva = None
        paivat = []
        kokoukset = []
        kokous = None
        kokousid = 0
        for rivi in res:
            if kokousid != int(rivi[6]):
                if kokous:
                    kokoukset.append(kokous)
                kokousid = int( rivi[6])
                kokous = {"id": rivi[6],
                          "ryhma" : rivi[1],
                          "alkaa" : parsedate( rivi[2]),
                          "paattyy": parsedate( rivi[3]),
                          "sijainti": rivi[4],
                          "kuvaus": rivi[5],
                          "osallistujat": [ rivi[0], ]}
            else:
                kokous["osallistujat"].append(rivi[0])

            if rivi[7] and current_user.id == int(rivi[8]) :
                kokous["ohjaaja"]=True

            kyspaiva = parsedate(rivi[2]).date()
            if kyspaiva != paiva and paiva:
                paivat.append( {"pvm":paiva, "kokoukset": kokoukset} )
                kokoukset = []
            paiva = kyspaiva
        if kokous:
            kokoukset.append(kokous)
            paivat.append({"pvm": paiva, "kokoukset": kokoukset})

        return paivat

    def omatryhmat(self) -> list:
        """Lista aktiivisista ryhmistä, joissa jäsenenä tai ohjaajana"""
        stmt = text("SELECT ryhma.id, ryhma.nimi, ryhmassa.ohjaaja,kokous.alkaa, kokous.sijainti, kokous.kuvaus, kokous.paattyy "
                    "FROM ryhmassa JOIN ryhma ON ryhmassa.ryhmaid=ryhma.id " 
                    "LEFT OUTER JOIN Kokous ON Kokous.ryhmaid = ryhma.id AND  Kokous.alkaa = (SELECT MIN(kokous.alkaa) FROM kokous WHERE kokous.alkaa > :tanaan AND kokous.ryhmaid = ryhma.id) "
                    "WHERE ryhmassa.henkiloid=:henkiloid AND NOT ryhma.paattynyt AND ryhmassa.paattyen IS NULL "
                    "ORDER BY nimi").params(henkiloid=self.id, tanaan=datetime.today())

        res = db.engine.execute(stmt)
        ryhmat = []
        for rivi in res:
            ryhmat.append({"id":rivi[0],
                           "nimi":rivi[1],
                           "ohjaaja":rivi[2],
                           "kokousalkaa":parsedate(rivi[3]),
                           "kokoussijainti": rivi[4],
                           "kokouskuvaus": rivi[5],
                           "kokouspaattyy": parsedate(rivi[6]) })
        return ryhmat