import logging

import requests
from django.conf import settings


logger = logging.getLogger(__name__)


def transmettre_evenement(event):
    url = settings.SMARTCUSTOMER_API_URL
    token = settings.SMARTCUSTOMER_API_TOKEN
    if not url or not token:
        event.derniere_erreur = "API SmartCustomer ou jeton non configuré."
        event.save(update_fields=["derniere_erreur"])
        logger.error("SmartCustomer delivery is not configured.")
        return False
    if not url.startswith("https://") and not (
        settings.DEBUG and url.startswith("http://127.0.0.1:")
    ):
        event.derniere_erreur = "Une URL HTTPS est nécessaire pour l'API distante."
        event.save(update_fields=["derniere_erreur"])
        logger.error("Refusing to send SmartShop events over a non-HTTPS connection.")
        return False

    payload = {
        "event_id": str(event.event_id),
        "session_id": event.session_id,
        "user_id": event.utilisateur_id,
        "type_evenement": event.type_evenement,
        "page": event.page,
        "produit_id": event.produit_id,
        "commande_id": event.commande_id,
        "valeur": str(event.valeur) if event.valeur is not None else None,
        "date_evenement": event.date_evenement.isoformat(),
    }

    event.tentatives += 1
    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Authorization": f"Bearer {token}"},
            timeout=settings.SMARTCUSTOMER_TIMEOUT,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        event.derniere_erreur = str(exc)[:300]
        event.save(update_fields=["tentatives", "derniere_erreur"])
        logger.warning(
            "Could not deliver SmartShop event %s: %s",
            event.event_id,
            event.derniere_erreur,
        )
        return False

    event.transmis = True
    event.derniere_erreur = ""
    event.save(update_fields=["transmis", "tentatives", "derniere_erreur"])
    return True
