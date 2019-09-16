from application import db
from sqlalchemy.sql import text

Lasnaolo = db.Table('lasnaolo',
    db.Column('ryhmassa', db.Integer, db.ForeignKey('ryhmassa.id', ondelete="SET NULL"), primary_key=True),
    db.Column('kokous', db.Integer, db.ForeignKey('kokous.id', ondelete="CASCADE"), primary_key=True) )


class Kokous(db.Model) :
    __tablename__ = "kokous"
    id = db.Column(db.Integer, primary_key=True)
    ryhmaid = db.Column(db.Integer, db.ForeignKey('ryhma.id', ondelete="CASCADE"), nullable=False)
    alkaa = db.Column( db.DateTime, nullable=False )
    paattyy = db.Column( db.DateTime, nullable=True)
    sijainti = db.Column( db.Text, nullable=True)
    kuvaus = db.Column( db.Text, nullable=True)
    memo = db.Column( db.Text, nullable=True)
    ryhma = db.relationship('Ryhma', backref='kokoukset', lazy=True)
    lasna = db.relationship('Ryhmassa', secondary=Lasnaolo, lazy=True,
                            backref=db.backref('kokoukset', lazy=True))

    def __init__(self, ryhmaId):
        self.ryhmaid = ryhmaId


    def paikallalista(self, ohjaaja):
        stmt = text("select etunimi, sukunimi, ryhmassa.id, lasna.ryhmassa, henkilo.varotieto from ryhmassa join henkilo on ryhmassa.henkiloid=henkilo.id "
                    "left outer join (select ryhmassa from lasnaolo where kokous=:kokousid) as lasna on lasna.ryhmassa=ryhmassa.id "
                    "where ryhmassa.ryhmaid=:ryhmaid and ohjaaja=:ohjaaja order by sukunimi,etunimi").params(kokousid=self.id, ryhmaid=self.ryhmaid, ohjaaja=ohjaaja)
        res = db.engine.execute(stmt)
        lista = []
        for rivi in res:
            lista.append({"etunimi": rivi[0],
                          "sukunimi":rivi[1],
                          "ryhmassa":rivi[2],
                          "lasna":rivi[3],
                          "varotieto":rivi[4]})
        return lista
