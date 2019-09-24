import math

# Bootstrapin sivutuslinkkien luominen

class Sivutus(object):
    """Näytettävän tiedon sivuttaminen Bootstrapin pagination-komponentin avulla

       Sivutusta ei kuitenkaan tehdä kauniisti tietokantakyselyillä.
       Näin, koska sivutettaessa kalenteria kalenterin yhteen päivään on yhdistetty useampia kyselyn rivejä
       (eri kokouksia ja eri henkilöiden osallistumisia), eikä kalenterin haluta sivutuksessa katkeavan
       päivien välistä.
       """
    def __init__(self, laajuus: int, sivu:int=1, sivulla:int=10):
        """ Sivutustoiminnallisuuden alustaminen

        :param laajuus: montako elementtiä sivutettavana
        :param sivu: millä sivulla ollaan
        :param sivulla: montako elementtiä sivua kohden
        """
        self.sivu = sivu
        self.laajuus = laajuus
        self.sivulla = sivulla

    def alku(self):
        """Sivun ensimmäinen elementti"""
        return (self.sivu-1) * self.sivulla

    def loppu(self):
        """Sivun viimeinen elementti"""
        loppuu = self.alku() + self.sivulla
        if loppuu > self.laajuus:
            return self.laajuus
        return loppuu

    def sivua(self):
        """Montako sivua yhteensä"""
        return int( math.ceil(1.0 * self.laajuus / self.sivulla) )

    def linkit(self):
        """Bootstrapilla muotoillut sivutuslinkin (edellinen, 1, 2, 3, seuraava)

            Linkit sisällytetään sivulle tempatessa tyyliin {{ sivutus.linkit() }}
        """
        if self.laajuus <= self.sivulla:
            return ""

        str = "<nav><ul class='pagination'><li class='page-item"
        if self.sivulla == 1:
            str+="disabled"
        str += "'><a class='page-link' href='?sivu=1' tabindex='-1' aria-disabled='true'>Edellinen</a></li>"

        for i in range(1,self.sivua()+1):
            str += "<li class='page-item"
            if self.sivu == i:
                str += " active' aria-current='page"
            str +="'><a class='page-link' href='?sivu={0}'>{0}</a></li>".format(i)

        str += "<li class='page-item"
        if self.sivulla == self.sivua():
            str+="disabled"
        str += "'><a class='page-link' href='?sivu={}' tabindex='-1' aria-disabled='true'>Seuraava</a></li>".format(self.sivua())
        str += "</ul></nav>"
        return str
