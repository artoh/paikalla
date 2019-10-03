from application import db
from application.models import Henkilo
from flask_login import current_user
from sqlalchemy.sql import text


def kayttaja_autorisointi(henkilo_id: int) -> Henkilo:
    """Autorisointi tilanteissa, joissa käyttäjä muokkaa omia tai huollettavan tietoja, taikka tekee
    ilmoittautumisen

    :param henkilo_id: Henkilön id, jonka tietoja muokataan
    :return Henkilo-olio henkiloon, jonka tietoja saa muokata, tai None ellei oikeutta muokkaamiseen
    """
    if not current_user or not current_user.is_authenticated:
        return None
    henkilo = Henkilo.query.get(henkilo_id)
    if not henkilo:
        return None
    if henkilo.aikuinen() and henkilo.id == current_user.id:
        return henkilo
    if not henkilo.aikuinen():
        for huoltaja in henkilo.huoltajat:
            if huoltaja.id == current_user.id :
                return henkilo
    return None


def ryhma_autorisaatio(ryhma_id: int) -> bool:
    """Autorisointi näkymissä, joita saa käyttää pääkäyttäjä taikka ryhmän ohjaaja

    :param ryhma_id: Ryhmän id, jota tarkastellaan
    :return Onko oikeutta ryhmän tietoihin
    """
    if not current_user or not current_user.is_authenticated:
        return False

    if current_user.toimihenkilo:
        return True

    res = db.engine.execute( text("SELECT id FROM ryhmassa WHERE ryhmaid=:ryhmaid AND "
                                  "henkiloid=:henkiloid AND ohjaaja")
                             .params(ryhmaid=ryhma_id, henkiloid=current_user.id))
    return res.first() is not None
