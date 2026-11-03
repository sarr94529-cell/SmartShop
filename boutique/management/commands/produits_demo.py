from django.core.management.base import BaseCommand
from boutique.models import Produit
class Command(BaseCommand):
    help='Créer des produits fictifs pour la démonstration.'
    def handle(self,*args,**kwargs):
        data=[('Samsung Galaxy A15','telephone',125000),('iPhone 13','telephone',280000),('Robe élégante','vetement',15000),('Ensemble homme','vetement',20000),('Baskets sport','chaussure',45000),('Sac à main','accessoire',18000),('Parfum doux','cosmetique',12000),('Montre connectée','accessoire',25000),('Lampe de bureau','maison',9000),('Casque Bluetooth','accessoire',14000),('Chaussures ville','chaussure',30000),('Chemise coton','vetement',12000)]
        for nom,categorie,prix in data:
            Produit.objects.get_or_create(nom=nom,defaults={'categorie':categorie,'prix':prix,'description':f'{nom} — article de démonstration SmartShop.','stock':20})
        self.stdout.write(self.style.SUCCESS('Catalogue créé : illustrations locales incluses, visibles sans Internet.'))
