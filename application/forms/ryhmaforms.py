from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, DateField, SubmitField, validators


class RyhmaTiedotForm(FlaskForm) :
    nimi = StringField("Ryhmän nimi", validators=[validators.DataRequired(message="Nimi vaaditaan"), validators.Length(min=3, message="Nimi vähintään kolme merkkiä pitkä")])
    paikkoja = IntegerField("Paikkoja", validators=[validators.NumberRange(min=0, max=999, message="Paikkoja voi olla 0-999")], default=0)
    ilmoittautuminenAlkaa = DateField("Ilmoittautuminen alkaa")
    ilmoittautuminenPaattyy = DateField("Ilmoittautuminen päättyy")
    kuvaus = TextAreaField("Ryhmän kuvaus")
    submit = SubmitField("Tallenna")

    def tayta(self, ryhma):
        self.nimi.data = ryhma.nimi

    class Meta:
        csrf = False
