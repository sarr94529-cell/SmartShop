# SmartShop — boutique Django prête pour VS Code

## Démarrage Windows CMD

1. Extraire le dossier `SmartShop` sur le Bureau. Ouvrir ce dossier dans VS Code.
2. Dans CMD :

```cmd
cd /d "%USERPROFILE%\Desktop\SmartShop"
python -m venv env
env\Scripts\activate
python -m pip install -r requirements.txt
copy .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py produits_demo
python manage.py createsuperuser
python manage.py check
python manage.py runserver
```

3. Visiter `http://127.0.0.1:8000/` ; administration `http://127.0.0.1:8000/admin/`.
4. Si les produits ne s'affichent pas, vérifier que `python manage.py produits_demo` a bien été exécutée.

## Fonctionnalités

Accueil, catalogue, recherche, filtres, fiches produits, panier en session, inscription, connexion, historique des commandes, validation de commande simulée, gestion du stock, administration, collecte des événements sous consentement, export vers une API SmartCustomer configurée.

**Images :** 12 illustrations de produits sont incluses localement dans `static/images/produits/` : elles fonctionnent sans Internet. Elles ne sont **pas des photographies**. Pour obtenir de vraies photos, ajouter des images depuis l'administration Django dans chaque fiche produit.

**Paiement :** simulation uniquement, aucun paiement réel.

**SmartCustomer :** l'API réceptrice est déployée sur `https://smartcustomer-analytics.onrender.com/api/smartshop/evenements/`. La transmission demande un jeton configuré côté serveur SmartShop et SmartCustomer. Voir `INTEGRATION_SMARTCUSTOMER.md`.

**Données locales :** les produits et commandes de démonstration sont stockés dans SQLite en local. Sur Render, les variables configurent PostgreSQL et les médias téléversés ne sont pas persistants sur le plan gratuit.

## Tests

```cmd
python manage.py test
```

## Déploiement gratuit sur Render

Le dépôt contient `render.yaml` pour créer SmartShop avec un service Web et PostgreSQL en offre gratuite. Depuis Render, crée un **Blueprint** relié au dépôt GitHub `sarr94529-cell/SmartShop` et vérifie que le service Web et la base sont tous deux sur le plan **Free** avant de confirmer.

Dans les variables d'environnement du service SmartCustomer sur Render, configure `SMARTSHOP_TRACKING_TOKEN`. Dans celles de SmartShop, configure `SMARTCUSTOMER_API_TOKEN` avec le même jeton privé. Ne place jamais ce jeton dans le code ou dans GitHub. Après le premier déploiement, exécute `python manage.py envoyer_evenements` périodiquement depuis un environnement ayant accès à la base de SmartShop. Sans cette commande, les événements restent enregistrés dans SmartShop et ne sont pas transmis à SmartCustomer.

**Limites de l’offre gratuite :** le service Web s'endort après une période d'inactivité et son système de fichiers est temporaire ; PostgreSQL gratuit expire après 30 jours. Ce déploiement convient à une démonstration, pas à une conservation durable des données. Les médias téléversés ne sont pas persistants sur le service gratuit.
