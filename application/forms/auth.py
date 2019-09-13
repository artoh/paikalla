from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, validators, SubmitField
from .jasenet import HenkiloTiedotFormBase, IkaValidator
from application.models.henkilo import Henkilo
from application import bcrypt
from datetime import datetime

class LuoKayttajaForm(HenkiloTiedotFormBase) :
    jasen = BooleanField("Liityn yhdistyksen jäseneksi", default=True)
    salasana = PasswordField("Salasana", validators=[ validators.Length(min=6, message="Salasanan oltava vähintään 6 merkkiä pitkä.") ])
    uudestaan = PasswordField("Syötä salasana uudelleen", validators=[ validators.EqualTo("salasana",message="Salasanat eivät ole samoja.") ])
    submit = SubmitField("Luo käyttäjä")

    def __init__(self, form = None):
        super().__init__(form)
        self.email.validators.append(validators.Email())
        self.syntymaaika.validators.append( IkaValidator(min=18, message="Vain täysi-ikäinen voi luoda itse tunnuksen") )

    def henkilo(self):
        henkilo = Henkilo()
        super().tallenna(henkilo)
        if self.jasen.data :
            henkilo.jasenyysAlkoi = datetime.today()
            henkilo.salasana = bcrypt.generate_password_hash( self.salasana.data)
        return henkilo

