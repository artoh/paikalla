from wtforms import BooleanField, PasswordField, validators, SubmitField
from .jasenet import HenkiloTiedotFormBase, IkaValidator
from wtforms.fields.html5 import EmailField, DateField
from application.models.henkilo import Henkilo
from datetime import datetime

class LuoKayttajaForm(HenkiloTiedotFormBase) :
    """Uuden henkilön luominen itserekisteröitymisen yhteydessä"""
    syntymaaika = DateField("Syntymäaika", validators=[validators.DataRequired(message="Anna päivämäärä"), IkaValidator(min=18)],format='%Y-%m-%d')
    jasen = BooleanField("Liityn yhdistyksen jäseneksi", default=True)
    email = EmailField("Sähköposti", validators=[validators.Email(message="Sähköpostiosoite ei ole kelvollinen"), validators.Length(max=64)] )
    salasana = PasswordField("Salasana", validators=[ validators.Length(min=6, message="Salasanan oltava vähintään 6 merkkiä pitkä.") ])
    uudestaan = PasswordField("Syötä salasana uudelleen", validators=[ validators.EqualTo("salasana",message="Salasanat eivät ole samoja.") ])
    submit = SubmitField("Luo käyttäjä")

    def __init__(self, form = None):
        super().__init__(form)

    def henkilo(self) -> Henkilo:
        """Palauttaa luotavaa käyttäjää vastaavan Henkilö-olion"""
        henkilo = Henkilo()
        super().tallenna(henkilo)
        if self.jasen.data:
            henkilo.jasenyysalkoi = datetime.today()
        henkilo.asetaSalasana( self.salasana.data )
        return henkilo
