from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, validators, SelectField, ValidationError
from wtforms.fields.html5 import DateTimeLocalField, DateField, TimeField
from application.models.kokous import Kokous

class KokousTiedotForm(FlaskForm):
    """Lomake kokoustietojen muokkaamiseen"""

    def alkaa_ennen_paattymista(self, field) -> None:
        """Validaattorifunktio varmistamaan, ettei kokous pääty ennen kuin se alkaa."""
        if (self.alkaa.data > self.paattyy.data):
            raise ValidationError("Kokous ei voi päättyä ennen kuin se alkoi")

    alkaa= DateTimeLocalField("Kokous alkaa", validators=[validators.InputRequired()], format='%Y-%m-%dT%H:%M')
    paattyy= DateTimeLocalField("Kokous päättyy", validators=[validators.InputRequired(), alkaa_ennen_paattymista], format='%Y-%m-%dT%H:%M')
    sijainti= StringField("Sijainti")
    kuvaus= TextAreaField("Ennakkotiedot")
    submit = SubmitField("Tallenna")

    def lataa(self, kokous: Kokous) -> None:
        """Täyttää lomakkeen kokouksen tiedoilla"""
        self.alkaa.data = kokous.alkaa
        self.paattyy.data = kokous.paattyy
        self.sijainti.data = kokous.sijainti
        self.kuvaus.data = kokous.kuvaus


    def tallenna(self, kokous: Kokous) -> None:
        """Tallentaa lomakkeen tiedot Kokous-olioon"""
        kokous.alkaa = self.alkaa.data
        kokous.paattyy = self.paattyy.data
        kokous.sijainti = self.sijainti.data
        kokous.kuvaus = self.kuvaus.data


class KokousSarjaForm(FlaskForm) :
    """Lomake toistuvien kokous luomiseksi tietyllä aikamäärävälillä aina samana viikonpäivänä samaan aikaan"""

    def alkaa_ennen_paattymista(self, field):
        """Validaattorifunktio varmistamaan, ettei kokoussarjan päättymispäivämäärä ole alkupäivämäärää aikaisempi"""
        if (self.alkaa.data > self.paattyy.data):
            raise ValidationError("Kokoussarja ei voi päättyä ennen kuin se alkoi")

    def klo_ennen_paattymista(self, field):
        """Validaattorifunktio varmistamaan, ettei kokouksen päättymiskellonaika ole alkuaikaa aikaisempi"""
        if (self.alkaaklo.data > self.paattyyklo.data):
            raise ValidationError("Kokous ei voi päättyä ennen kuin se alkoi")

    alkaa= DateField("Alkaa päivästä", [validators.InputRequired()])
    paattyy= DateField("Päättyy päivään", [alkaa_ennen_paattymista, validators.InputRequired() ])
    viikonpaiva= SelectField("Viikonpäivä",
                             choices=[("0","Maanantai"),
                                      ("1", "Tiistai"),
                                      ("2", "Keskiviikko"),
                                      ("3", "Torstai"),
                                      ("4", "Perjantai"),
                                      ("5", "Lauantai"),
                                      ("6", "Sunnuntai")])
    alkaaklo= TimeField("Alkaa klo", [validators.InputRequired() ])
    paattyyklo= TimeField("Päättyy klo", [klo_ennen_paattymista, validators.InputRequired() ])
    sijainti= StringField("Sijanti")
    kuvaus= TextAreaField("Ennakkotiedot")
    submit= SubmitField("Tallenna")