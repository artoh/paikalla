from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, validators, SelectField
from wtforms.fields.html5 import DateTimeLocalField, DateField, TimeField

class KokousTiedotForm(FlaskForm):
    alkaa= DateTimeLocalField("Kokous alkaa", format='%Y-%m-%dT%H:%M')
    paattyy= DateTimeLocalField("Kokous päättyy", format='%Y-%m-%dT%H:%M')
    sijainti= StringField("Sijainti")
    kuvaus= TextAreaField("Ennakkotiedot")
    submit = SubmitField("Tallenna")

    def lataa(self, kokous):
        self.alkaa.data = kokous.alkaa
        self.paattyy.data = kokous.paattyy
        self.sijainti.data = kokous.sijainti
        self.kuvaus.data = kokous.kuvaus

    def tallenna(self, kokous):
        kokous.alkaa = self.alkaa.data
        kokous.paattyy = self.paattyy.data
        kokous.sijainti = self.sijainti.data
        kokous.kuvaus = self.kuvaus.data


class KokousSarjaForm(FlaskForm) :
    alkaa= DateField("Alkaa päivästä")
    paattyy= DateField("Päättyy päivään")
    viikonpaiva= SelectField("Viikonpäivä",
                             choices=[("1","Maanantai"),
                                      ("2", "Tiistai"),
                                      ("3", "Keskiviikko"),
                                      ("4", "Torstai"),
                                      ("5", "Perjantai"),
                                      ("6", "Lauantai"),
                                      ("0", "Sunnuntai")])
    alkaaklo= TimeField("Alkaa klo")
    paattyyklo= TimeField("Päättyy klo")
    sijainti= StringField("Sijanti")
    kuvaus= TextAreaField("Ennakkotiedot")
    submit= SubmitField("Tallenna")