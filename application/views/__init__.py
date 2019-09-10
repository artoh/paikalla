from .ryhmat import *
from .jasenet import *

@app.template_filter('pvm')
def format_date(value, format="%d.%m.%Y"):
    if value is None:
        return ""
    return value.strftime(format)