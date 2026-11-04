# Liaison SmartShop et SmartCustomer Analytics

SmartShop enregistre les événements uniquement après consentement, puis les transmet immédiatement au serveur SmartCustomer. Le jeton reste côté serveur ; ne l'ajoutez jamais au JavaScript du navigateur.

## Configuration

Dans le fichier `.env` local de SmartShop :

```env
SMARTCUSTOMER_API_URL=https://smartcustomer-analytics.onrender.com/api/smartshop/evenements/
SMARTCUSTOMER_API_TOKEN=le-meme-jeton-long-aleatoire-que-sur-render
```

Dans les variables d'environnement du service SmartCustomer sur Render, définir `SMARTSHOP_TRACKING_TOKEN` avec la même valeur. Créez un jeton aléatoire long et gardez-le privé. Le dépôt ne contient volontairement aucun jeton.

## Transmission

Chaque événement accepté est envoyé immédiatement. Si l'API n'est pas disponible, il reste marqué comme non transmis dans la base SmartShop et la commande suivante permet de réessayer jusqu'à 100 événements :

```cmd
python manage.py envoyer_evenements
```

Un événement n'est marqué comme transmis qu'après une réponse HTTP réussie ; les échecs sont consignés dans les journaux et restent disponibles pour réessai. SmartCustomer déduplique les nouvelles tentatives à partir de `event_id`.

Sur Render, ne configurez pas SmartShop avec l'URL de base de données `smartcustomer-db` : les deux applications Django auraient des tables partagées. Sans base dédiée, SmartShop utilise SQLite temporaire ; les événements transmis restent stockés dans la base SmartCustomer, mais les événements en attente et les données de commande SmartShop peuvent être perdus au redémarrage du service.

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
