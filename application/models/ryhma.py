from application import db
from .ryhmassa import Ryhmassa
from .henkilo import Henkilo

class Ryhma(db.Model):
    __tablename__ = "Ryhma"
    id = db.Column(db.Integer, primary_key=True)
    nimi = db.Column( db.String(128), nullable=False)
    paikkoja = db.Column( db.Integer, default=0)
    ilmoittautuminenAlkaa = db.Column( db.DateTime, nullable=True)
    ilmoittautuminenPaattyy = db.Column( db.DateTime, nullable=True)
    kuvaus = db.Column(db.Text, nullable = True)
    paattynyt = db.Column( db.Boolean, default=False)

    def ohjaajat(self):
        ryhmassa = Ryhmassa.query.filter_by(ryhma=self.id).filter_by(ohjaaja=True)
        taulu = []
        for r in ryhmassa:
            print(r.jasen)
            taulu.append( Henkilo.query.get(r.jasen))
        taulu.sort(key=lambda x: x.sukunimi + " " + x.etunimi)
        return taulu

    def jasenet(self):
        ryhmassa = Ryhmassa.query.filter_by(ryhma=self.id).filter_by(ohjaaja=False)
        taulu = []
        for r in ryhmassa:
            print(r.jasen)
            taulu.append( Henkilo.query.get(r.jasen))
        taulu.sort(key=lambda x: x.sukunimi + " " + x.etunimi)
        return taulu