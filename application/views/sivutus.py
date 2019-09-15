import math

# Bootstrapin sivutuslinkkien luominen

class Sivutus(object):
    def __init__(self, laajuus, sivu=1, sivulla=10):
        self.sivu = sivu
        self.laajuus = laajuus
        self.sivulla = sivulla

    def alku(self):
        return (self.sivu-1) * self.sivulla

    def loppu(self):
        loppuu = self.alku() + self.sivulla
        if loppuu > self.laajuus:
            return self.laajuus
        return loppuu

    def sivua(self):
        return int( math.ceil(1.0 * self.laajuus / self.sivulla) )

    def linkit(self):
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
