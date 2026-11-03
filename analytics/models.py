import uuid
from django.conf import settings
from django.db import models
class EvenementNavigation(models.Model):
    TYPES=[('page_view','Page visitée'),('product_view','Produit consulté'),('add_to_cart','Ajout panier'),('remove_from_cart','Retrait panier'),('cart_update','Modification panier'),('purchase','Commande simulée')]
    event_id=models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    utilisateur=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    session_id=models.CharField(max_length=100)
    type_evenement=models.CharField(max_length=30,choices=TYPES)
    page=models.CharField(max_length=255,blank=True)
    produit_id=models.IntegerField(null=True,blank=True)
    commande_id=models.IntegerField(null=True,blank=True)
    valeur=models.DecimalField(max_digits=12,decimal_places=0,null=True,blank=True)
    date_evenement=models.DateTimeField(auto_now_add=True)
    transmis=models.BooleanField(default=False,db_index=True)
    tentatives=models.PositiveIntegerField(default=0)
    derniere_erreur=models.CharField(max_length=300,blank=True)
    def __str__(self): return f'{self.type_evenement} ({self.session_id})'
