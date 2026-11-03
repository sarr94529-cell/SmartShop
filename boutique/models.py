from django.conf import settings
from django.db import models

class Produit(models.Model):
    CATEGORIES=[('telephone','Téléphones'),('vetement','Vêtements'),('chaussure','Chaussures'),('cosmetique','Cosmétiques'),('accessoire','Accessoires'),('maison','Maison')]
    nom=models.CharField(max_length=200)
    description=models.TextField(blank=True)
    prix=models.DecimalField(max_digits=12,decimal_places=0)
    categorie=models.CharField(max_length=30,choices=CATEGORIES)
    image=models.ImageField(upload_to='produits/',blank=True,null=True)
    stock=models.PositiveIntegerField(default=0)
    actif=models.BooleanField(default=True)
    date_creation=models.DateTimeField(auto_now_add=True)
    @property
    def image_demo_url(self):
        """Illustrations locales disponibles sans connexion Internet."""
        from django.templatetags.static import static
        noms = ['Samsung Galaxy A15', 'iPhone 13', 'Robe élégante', 'Ensemble homme',
                'Baskets sport', 'Sac à main', 'Parfum doux', 'Montre connectée',
                'Lampe de bureau', 'Casque Bluetooth', 'Chaussures ville', 'Chemise coton']
        try:
            numero = noms.index(self.nom) + 1
        except ValueError:
            return static('images/produits/produit_01.jpg')
        return static(f'images/produits/produit_{numero:02d}.jpg')

    def __str__(self): return self.nom

class Commande(models.Model):
    STATUTS=[('simulation','Simulation confirmée'),('annulee','Annulée')]
    utilisateur=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='commandes')
    nom=models.CharField(max_length=150)
    telephone=models.CharField(max_length=30)
    adresse=models.TextField()
    statut=models.CharField(max_length=20,choices=STATUTS,default='simulation')
    total=models.DecimalField(max_digits=12,decimal_places=0)
    cree_le=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'Commande #{self.pk}'

class LigneCommande(models.Model):
    commande=models.ForeignKey(Commande,on_delete=models.CASCADE,related_name='lignes')
    produit=models.ForeignKey(Produit,on_delete=models.PROTECT)
    nom_produit=models.CharField(max_length=200)
    quantite=models.PositiveIntegerField()
    prix_unitaire=models.DecimalField(max_digits=12,decimal_places=0)
    def sous_total(self): return self.prix_unitaire*self.quantite
