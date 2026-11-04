from .models import EvenementNavigation
from .delivery import transmettre_evenement

def enregistrer_evenement(request,type_evenement,produit_id=None,commande_id=None,valeur=None):
    # Respect du choix explicite de consentement analytique.
    if request.session.get('analytics_consent') is not True:
        return None
    if not request.session.session_key:
        request.session.create()
    event = EvenementNavigation.objects.create(
        utilisateur=request.user if request.user.is_authenticated else None,
        session_id=request.session.session_key,
        type_evenement=type_evenement,
        page=request.path[:255],
        produit_id=produit_id,
        commande_id=commande_id,
        valeur=valeur,
    )
    transmettre_evenement(event)
    return event
