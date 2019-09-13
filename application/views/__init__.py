from .ryhmat import *
from .jasenet import *
from .auth import *
from .mina import *


@app.template_filter('pvm')
def format_date(value, format="%d.%m.%Y"):
    if value is None:
        return ""
    return value.strftime(format)

@app.template_filter('pvmaika')
def format_date(value, format="%d.%m.%Y klo %H.%M"):
    if value is None:
        return ""
    return value.strftime(format)


