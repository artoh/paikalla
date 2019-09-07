from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, validators
from wtforms.fields.html5 import DateField, IntegerField

import datetime

class NullableDateField(DateField):
    """ WtFormsin DateField ei hyväksy tyhjää päivämäärää, jota tarvitaan
    osoittamaan puuttuva päivämäärä.

    https://stackoverflow.com/questions/27766417/how-to-implement-not-required-datefield-using-flask-wtf """
    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist).strip()
            if date_str == '':
                self.data = None
                return
            try:
                self.data = datetime.datetime.strptime(date_str, self.format).date()
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Päivämäärä ei ole kelvollinen'))

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
