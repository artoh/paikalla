from application import db
from datetime import date
from sqlalchemy.sql import text

Huoltajuus = db.Table('Huoltajuus',
      db.Column( 'huoltaja', db.Integer, db.ForeignKey('Henkilo.id', ondelete="CASCADE"), primary_key=True),
      db.Column( 'huollettava', db.Integer, db.ForeignKey('Henkilo.id', ondelete="CASCADE"), primary_key=True))

def ika(syntymapaiva):
    tanaan = date.today()
    vuotta = tanaan.year - syntymapaiva.year
    if tanaan.month < syntymapaiva.month or tanaan.month == syntymapaiva.month and tanaan.day < syntymapaiva.day:
        vuotta -= 1
    return vuotta


class Henkilo(db.Model):
    __tablename__ = "Henkilo"
    id = db.Column(db.Integer, primary_key=True)
    etunimi = db.Column( db.String(128), nullable=False)
    sukunimi = db.Column( db.String(128), nullable=False)
    puhelin = db.Column( db.String(32), nullable=True)
    email = db.Column( db.String(64), nullable=True, unique=True)
    salasana = db.Column( db.Text, nullable=True)
    syntymaaika = db.Column( db.Date, nullable=False)
    toimihenkilo = db.Column( db.Boolean, default=False )
    varotieto = db.Column (db.Text, nullable=True)
    jasenyysAlkoi = db.Column( db.Date, nullable=True)
    jasenyysPaattyi = db.Column( db.Date, nullable=True)
    huoltajat = db.relationship('Henkilo',
                            secondary=Huoltajuus,
                            primaryjoin=id == Huoltajuus.c.huollettava,
                            secondaryjoin=id == Huoltajuus.c.huoltaja,
                            backref=db.backref('huollettavat'))
    ryhmat = db.relationship('Ryhmassa', backref='ryhmat', lazy=True)

    def ika(self):
        return ika(self.syntymaaika)

    def aikuinen(self):
        return self.ika() >= 18


    def get_id(self):
        return self.id

    # Vain aikuinen jolla on salasana voi kirjautua
    def is_active(self):
        return self.aikuinen and len( self.salasana )

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def mahdollisetryhmat(self):
        stmt = text("select ryhma.id,nimi,paikkoja,kuvaus,a.lkm  "
                    "from ryhma left outer join "
                    "(select ryhmaid, count(id) as lkm from ryhmassa where ohjaaja = 0 and  paattyen is null group by ryhmaid) as a on ryhma.id=a.ryhmaid "
                    "where ilmoittautuminenalkaa <= current_date and ilmoittautuminenpaattyy >= current_date "
                    "and ikavahintaan <= :ika and ikaenintaan >= :ika "
                    "and ryhma.id not in (select ryhmaid from ryhmassa where henkiloid=:henkiloid) "
                    "order by nimi"
                    ).params(ika=self.ika(), henkiloid=self.id)
        res = db.engine.execute(stmt)
        lista = []
        for rivi in res:
            if rivi[4] :
                lkm = rivi[4]
            else:
                lkm = 0
            lista.append({"ryhmaId": rivi[0],
                          "nimi":rivi[1],
                          "paikkoja":rivi[2],
                          "kuvaus":rivi[3],
                          "lkm":lkm})
        return lista