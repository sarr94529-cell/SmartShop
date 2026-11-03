from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns=[
 path('',views.accueil,name='accueil'),
 path('produits/',views.produits,name='produits'),
 path('produit/<int:pk>/',views.detail_produit,name='detail_produit'),
 path('panier/',views.panier,name='panier'),
 path('panier/ajouter/<int:produit_id>/',views.ajouter_panier,name='ajouter_panier'),
 path('panier/modifier/<int:produit_id>/',views.modifier_panier,name='modifier_panier'),
 path('panier/supprimer/<int:produit_id>/',views.supprimer_panier,name='supprimer_panier'),
 path('inscription/',views.inscription,name='inscription'),
 path('connexion/',auth_views.LoginView.as_view(template_name='connexion.html'),name='connexion'),
 path('deconnexion/',auth_views.LogoutView.as_view(),name='deconnexion'),
 path('commander/',views.commander,name='commander'),
 path('mes-commandes/',views.mes_commandes,name='mes_commandes'),
 path('consentement/',views.consentement,name='consentement'),
]
