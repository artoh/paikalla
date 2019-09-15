from application.models import Henkilo
from flask_login import current_user


def kayttaja_autorisointi(henkilo_id):
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