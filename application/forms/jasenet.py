from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField, validators, ValidationError
from wtforms.fields.html5 import EmailField, DateField
from application.models.henkilo import ika, Henkilo

from . import NullableDateField


class IkaValidator(object):
    """Validaattori, jolla voidaan vaatia syntymäaika syötettäväksi tietylle ikävälille"""
    def __init__(self, min=0, max=120, message=None):
        self.min = min
        self.max = max
        if not message:
            message = "Iän oltava väliltä {} ja {}".format(min,max)
        self.message = message

    def __call__(self, form, field):
        vuotta = ika(field.data)
        if vuotta < self.min or vuotta > self.max:
            raise ValidationError(self.message)


class HenkiloTiedotFormBase(FlaskForm) :
    """Kantaluokka erilaisille henkilötietojen lomakkeille"""
    etunimi = StringField("Etunimi", validators=[ validators.DataRequired(), validators.Length(min=1,max=128)])
    sukunimi = StringField("Sukunimi", validators=[validators.DataRequired(), validators.Length(min=1,max=128)])
    syntymaaika = DateField("Syntymäaika", validators=[validators.InputRequired(), IkaValidator()], format='%Y-%m-%d')
    puhelin = StringField("Puhelinnumero", [validators.Length(min=0,max=32)] )
    email = EmailField("Sähköposti", validators=[validators.Email( message="Sähköpostiosoite ei ole kelvollinen"),
                                                 validators.Optional(), validators.length(max=64)])
    varotieto = TextAreaField("Huomioon otettavaa (esim. allergiat)")

    def lataa(self, henkilo : Henkilo) -> None:
        """Täyttää lomakeen kentät olemassaolevan Henkilön perusteella"""
        self.etunimi.data = henkilo.etunimi
        self.sukunimi.data = henkilo.sukunimi
        self.syntymaaika.data = henkilo.syntymaaika
        self.puhelin.data = henkilo.puhelin
        self.email.data = henkilo.email
        self.varotieto.data = henkilo.varotieto

    def tallenna(self, henkilo) -> None:
        """Tallentaa lomakkeen kentätä Henkilö-olioon"""
        henkilo.etunimi = self.etunimi.data
        henkilo.sukunimi = self.sukunimi.data
        henkilo.syntymaaika = self.syntymaaika.data
        henkilo.puhelin = self.puhelin.data
        if self.email.data and len(self.email.data) > 5 :
            henkilo.email = self.email.data
        henkilo.varotieto = self.varotieto.data


class HenkiloTiedotForm(HenkiloTiedotFormBase) :
    """Perusmuotoinen lomake henkilötietojen muokkaamiseen"""
    submit = SubmitField("Tallenna")


class HenkiloTiedotLapsiForm(HenkiloTiedotFormBase):
    """Henkilötietolomake, joka vaatii henkilön olevan alle 18-vuotias.
       Käytetään, kun ollaan lisäämässä huollettavaa."""
    syntymaaika = DateField("Syntymäaika", validators=[validators.InputRequired(), IkaValidator(max=17)],format='%Y-%m-%d')
    submit = SubmitField("Tallenna")


class HenkiloTiedotAikuiselleForm(HenkiloTiedotFormBase):
    """Henkilötietolomake, joka vaatii henkilön olevan vähintään 18-vuotias.
       Käytetään, kun ollaan lisäämässä huoltajaa."""
    syntymaaika = DateField("Syntymäaika", validators=[validators.InputRequired(), IkaValidator(min=18)],format='%Y-%m-%d')
    submit = SubmitField("Tallenna")


class HenkiloTiedotAdminilleForm(HenkiloTiedotFormBase) :
    """Henkilötietolomake, kun toimihenkilö muokkaa henkilöä.
       Mahdollisuus myös jäsenyystietojen muuttamiseen."""

    def alkaa_ennen_paattymista(self, field):
        if( self.jasenyysPaattyi.data and self.jasenyysPaattyi.data < self.jasenyysAlkoi.data):
            raise ValidationError("Jäsenyys ei voi päättyä ennen kuin se alkoi")
        elif self.jasenyysPaattyi.data and not self.jasenyysAlkoi.data:
            raise ValidationError("Jäsenyys ei voi päättyä, ellei se ole alkanut")

    jasenyysAlkoi = NullableDateField("Jäsenyys alkoi")
    jasenyysPaattyi = NullableDateField("Jäsenyys päättyi",[alkaa_ennen_paattymista])
    toimihenkilo = BooleanField("Jäsentietojen käsittelyyn oikeutettu yhdistyksen toimihenkilö")
    submit = SubmitField("Tallenna")

    def lataa(self, henkilo: Henkilo) -> None:
        super().lataa(henkilo)
        self.jasenyysAlkoi.data = henkilo.jasenyysalkoi
        self.jasenyysPaattyi.data = henkilo.jasenyyspaattyi
        self.toimihenkilo.data = henkilo.toimihenkilo

    def tallenna(self, henkilo: Henkilo) -> None:
        super().tallenna(henkilo)
        henkilo.jasenyysalkoi = self.jasenyysAlkoi.data
        henkilo.jasenyyspaattyi = self.jasenyysPaattyi.data
        henkilo.toimihenkilo = self.toimihenkilo.data
