from dateutil.parser import parse

def parsedate(pvm):
    """Palauttaa syötteensä päivämääränä

      Funktiota tarvitaan haettaessa tietoa SQL-kyselyistä, koska SQLite palauttaa päivämäärät
      merkkijonoina mutta PostgreSQL päivämääräolioina"""
    if isinstance(pvm,str):
        return parse(pvm)
    return pvm

from .ryhma import Ryhma
from .henkilo import Henkilo
from .ryhmassa import Ryhmassa
from .kokous import Kokous

