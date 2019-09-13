from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField, validators
from wtforms.fields.html5 import EmailField

from . import NullableDateField

class HenkiloTiedotFormBase(FlaskForm) :
    etunimi = StringField("Etunimi", validators=[ validators.DataRequired()])
    sukunimi = StringField("Sukunimi", validators=[validators.DataRequired()])
    puhelin = StringField("Puhelinnumero")
    # email tarkastetaan regexpillä, jotta voi jäädä tyhjäksi
    email = EmailField("Sähköposti", validators=[validators.Regexp("(\S+@\S+\.\w+)?", message="Sähköpostiosoite ei ole kelvollinen")])
    varotieto = TextAreaField("Huomioon otettavaa (esim. allergiat)")

    class Meta:
        csrf = False

    def lataa(self, henkilo):
        self.etunimi.data = henkilo.etunimi
        self.sukunimi.data = henkilo.sukunimi
        self.puhelin.data = henkilo.puhelin
        self.email.data = henkilo.email
        self.varotieto.data = henkilo.varotieto

    def tallenna(self, henkilo):
        henkilo.etunimi = self.etunimi.data
        henkilo.sukunimi = self.sukunimi.data
        henkilo.puhelin = self.puhelin.data
        henkilo.email = self.email.data
        henkilo.varotieto = self.varotieto.data


class HenkiloTiedotForm(HenkiloTiedotFormBase) :
    submit = SubmitField("Tallenna")

class HenkiloTiedotAdminilleForm(HenkiloTiedotFormBase) :
    jasenyysAlkoi = NullableDateField("Jäsenyys alkoi")
    jasenyysPaattyi = NullableDateField("Jäsenyys päättyi")
    aikuinen = BooleanField("Aikuinen")
    toimihenkilo = BooleanField("Jäsentietojen käsittelyyn oikeutettu yhdistyksen toimihenkilö")
    submit = SubmitField("Tallenna")

    def lataa(self, henkilo):
        super().lataa(henkilo)
        self.jasenyysAlkoi.data = henkilo.jasenyysAlkoi
        self.jasenyysPaattyi.data = henkilo.jasenyysPaattyi
        self.aikuinen.data = henkilo.aikuinen
        self.toimihenkilo.data = henkilo.toimihenkilo

    def tallenna(self, henkilo):
        super().tallenna(henkilo)
        henkilo.jasenyysAlkoi = self.jasenyysAlkoi.data
        henkilo.jasenyysPaattyi = self.jasenyysPaattyi.data
        henkilo.aikuinen = self.aikuinen.data
        henkilo.toimihenkilo = self.toimihenkilo.data

    class Meta:
        csrf = False