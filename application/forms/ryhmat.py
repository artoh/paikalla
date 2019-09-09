from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, validators
from wtforms.fields.html5 import IntegerField

from . import NullableDateField

class RyhmaTiedotForm(FlaskForm) :
    nimi = StringField("Ryhmän nimi", validators=[validators.Length(min=3, message="Nimi vähintään kolme merkkiä pitkä")])
    paikkoja = IntegerField("Paikkoja", validators=[validators.NumberRange(min=0, message="Paikkoja ei voi olla negatiivista määrää")], default=0)
    ilmoittautuminenAlkaa = NullableDateField("Ilmoittautuminen alkaa")
    ilmoittautuminenPaattyy = NullableDateField("Ilmoittautuminen päättyy")
    kuvaus = TextAreaField("Ryhmän kuvaus")
    paattynyt = BooleanField("Ryhmä on päättynyt")
    submit = SubmitField("Tallenna")


    def lataa(self, ryhma):
        self.nimi.data = ryhma.nimi
        self.paikkoja.data = ryhma.paikkoja
        self.ilmoittautuminenAlkaa.data = ryhma.ilmoittautuminenAlkaa
        self.ilmoittautuminenPaattyy.data = ryhma.ilmoittautuminenPaattyy
        self.kuvaus.data = ryhma.kuvaus
        self.paattynyt.data = ryhma.paattynyt

    def tallenna(self, ryhma):
        ryhma.nimi = self.nimi.data
        ryhma.paikkoja = self.paikkoja.data
        ryhma.ilmoittautuminenAlkaa = self.ilmoittautuminenAlkaa.data
        ryhma.ilmoittautuminenPaattyy = self.ilmoittautuminenPaattyy.data
        ryhma.kuvaus = self.kuvaus.data
        ryhma.paattynyt = self.paattynyt.data

    class Meta:
        csrf = False
