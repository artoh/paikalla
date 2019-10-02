from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, validators, ValidationError
from wtforms.fields.html5 import IntegerField
from application.models.ryhma import Ryhma

from . import NullableDateField

class RyhmaTiedotForm(FlaskForm) :
    """Rymän tietojen muokkauslomake"""

    def ilmo_validointi(self, field):
        """Validointifunktio ilmoittautumispäivämäärien validointiin: ilmoittautuminen ei voi päättyä,
           ennen kuin se on alkanut."""
        if self.ilmoittautuminenPaattyy.data and self.ilmoittautuminenPaattyy.data < self.ilmoittautuminenPaattyy.data:
            raise ValidationError("Ilmoittautuminen ei voi päättyä ennen kuin se alkoi")
        if self.ilmoittautuminenPaattyy.data and not self.ilmoittautuminenAlkaa.data :
            raise ValidationError("Ilmoittautuminen ei voi päättyä, ellei se ole alkanut")

    def ika_validointi(self, field):
        """Validointifunktio ikävaatimuksen validiointiin"""
        if self.ikaenintaan.data < self.ikavahintaan.data:
            raise ValidationError("Ikä vähintään ei voi olla enempää kuin ikä enintään.")

    nimi = StringField("Ryhmän nimi", validators=[validators.Length(min=3, max=128, message="Ryhmän nimi 3-128 merkkiä pitkä")])
    paikkoja = IntegerField("Paikkoja", validators=[validators.NumberRange(min=0, max=100, message="Ryhmässä voi olla 0 - 100 paikkaa")], default=0)
    ilmoittautuminenAlkaa = NullableDateField("Ilmoittautuminen alkaa")
    ilmoittautuminenPaattyy = NullableDateField("Ilmoittautuminen päättyy", [ilmo_validointi])
    ikavahintaan = IntegerField("Ikä vähintään", validators=[validators.NumberRange(min=0, max=120)], default=0)
    ikaenintaan = IntegerField("Ikä enintään", validators=[validators.NumberRange(min=0, max=120), ika_validointi], default=99)
    kuvaus = TextAreaField("Ryhmän kuvaus")
    paattynyt = BooleanField("Ryhmä on päättynyt")
    submit = SubmitField("Tallenna")


    def lataa(self, ryhma: Ryhma) -> None:
        """Täyttää lomakkeen kentät Ryhma-olion tiedoilla"""
        self.nimi.data = ryhma.nimi
        self.paikkoja.data = ryhma.paikkoja
        self.ilmoittautuminenAlkaa.data = ryhma.ilmoittautuminenalkaa
        self.ilmoittautuminenPaattyy.data = ryhma.ilmoittautuminenpaattyy
        self.ikavahintaan.data = ryhma.ikavahintaan
        self.ikaenintaan.data = ryhma.ikaenintaan
        self.kuvaus.data = ryhma.kuvaus
        self.paattynyt.data = ryhma.paattynyt


    def tallenna(self, ryhma: Ryhma) -> None:
        """Tallentaa lomakkeen tiedot Ryhma-olioon"""
        ryhma.nimi = self.nimi.data
        ryhma.paikkoja = self.paikkoja.data
        ryhma.ilmoittautuminenalkaa = self.ilmoittautuminenAlkaa.data
        ryhma.ilmoittautuminenpaattyy = self.ilmoittautuminenPaattyy.data
        ryhma.ikavahintaan = self.ikavahintaan.data
        ryhma.ikaenintaan = self.ikaenintaan.data
        ryhma.kuvaus = self.kuvaus.data
        ryhma.paattynyt = self.paattynyt.data

    class Meta:
        csrf = False
