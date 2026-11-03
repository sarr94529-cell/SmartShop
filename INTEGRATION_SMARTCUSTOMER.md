# Liaison SmartShop et SmartCustomer Analytics

SmartShop enregistre les événements uniquement après consentement et les envoie ensuite à l'API SmartCustomer par une commande Django. Le jeton reste côté serveur ; ne l'ajoutez jamais au JavaScript du navigateur.

## Configuration

Dans le fichier `.env` local de SmartShop :

```env
SMARTCUSTOMER_API_URL=https://smartcustomer-analytics.onrender.com/api/smartshop/evenements/
SMARTCUSTOMER_API_TOKEN=le-meme-jeton-long-aleatoire-que-sur-render
```

Dans les variables d'environnement du service SmartCustomer sur Render, définir `SMARTSHOP_TRACKING_TOKEN` avec la même valeur. Créez un jeton aléatoire long et gardez-le privé. Le dépôt ne contient volontairement aucun jeton.

## Transmission

La commande `envoyer_evenements` envoie au plus 100 événements non transmis par exécution. Elle peut être relancée sans dupliquer les événements : SmartCustomer déduplique à partir de `event_id`.

```cmd
python manage.py envoyer_evenements
```

Planifiez cette commande périodiquement sur le serveur SmartShop en production. En local, elle permet de vérifier la liaison avec l'API Render. Un événement n'est marqué comme transmis qu'après une réponse HTTP réussie ; les échecs restent disponibles pour réessai.

## Données envoyées

```json
{
  "event_id": "4b66f14a-9445-4c1a-8cb8-079d74ab33ab",
  "session_id": "session-django",
  "user_id": 2,
  "type_evenement": "product_view",
  "page": "/produit/1/",
  "produit_id": 1,
  "commande_id": null,
  "valeur": null,
  "date_evenement": "2026-10-29T12:00:00+00:00"
}
```

L'API requiert `Authorization: Bearer <jeton>`, valide le format et les types, refuse les événements inconnus et enregistre chaque identifiant une seule fois. Les événements sont consultables dans l'administration Django SmartCustomer.

## Événements pris en charge

- `page_view` : affichage d'une page.
- `product_view` : consultation d'une fiche produit.
- `add_to_cart`, `remove_from_cart`, `cart_update` : interaction avec le panier.
- `purchase` : commande **simulée** et montant.

Le consentement est demandé aux visiteurs avant tout enregistrement. Les données de navigation ne sont pas associées automatiquement à un client SmartCustomer : `user_id` reste l'identifiant local SmartShop. Le paiement est une simulation ; cette intégration ne mesure pas le temps actif et n'entraîne pas un modèle IA.
