from django.contrib import admin
from .models import Produit,Commande,LigneCommande
@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display=('nom','categorie','prix','stock','actif')
    list_filter=('categorie','actif')
    search_fields=('nom',)
class LigneInline(admin.TabularInline):
    model=LigneCommande
    extra=0
    readonly_fields=('produit','nom_produit','quantite','prix_unitaire')
    can_delete=False
@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display=('id','utilisateur','total','statut','cree_le')
    readonly_fields=('utilisateur','nom','telephone','adresse','total','cree_le')
    inlines=[LigneInline]
