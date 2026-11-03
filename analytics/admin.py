from django.contrib import admin
from .models import EvenementNavigation
@admin.register(EvenementNavigation)
class EvenementAdmin(admin.ModelAdmin):
    list_display=('type_evenement','session_id','produit_id','date_evenement','transmis','tentatives')
    list_filter=('type_evenement','transmis')
    readonly_fields=('event_id','session_id','utilisateur','type_evenement','page','produit_id','commande_id','valeur','date_evenement','transmis','tentatives','derniere_erreur')
