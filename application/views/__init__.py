from .ryhmat import *
from .jasenet import *
from .auth import *
from .henkilotiedot import *
from .ilmoittautumiset import *
from .kalenteri import *


@app.template_filter('pvm')
def format_date(value, format="%d.%m.%Y") -> str:
    """Filtteri päivämäärien näyttämiseen"""
    if value is None:
        return ""
    return value.strftime(format)

@app.template_filter('klo')
def format_date(value, format="%H.%M") -> str:
    """Filtteri kellonaikojen näyttämiseen """
    if value is None:
        return ""
    return value.strftime(format)

@app.template_filter('pvmaika')
def format_date(value, format="%a %d.%m.%Y klo %H.%M") -> str:
    """Filtteri päivämäärän ja kellonajan näyttämiseen yhdessä"""
    if value is None:
        return ""
    return value.strftime(format)
