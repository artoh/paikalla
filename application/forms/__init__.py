from wtforms.fields.html5 import DateField
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
