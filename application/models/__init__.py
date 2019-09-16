from dateutil.parser import parse

# Postgresql-yhteensopivuuden kääreeksi
# Koska sqlite palauttaa merkkijonon ja postgre päivämäärän,
# pareseoidaan vain päivämäärät
def parsedate(pvm):
    if isinstance(pvm,str):
        return parse(pvm)
    return pvm

from .ryhma import Ryhma
from .henkilo import Henkilo
from .ryhmassa import Ryhmassa
from .kokous import Kokous

