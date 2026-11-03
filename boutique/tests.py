from django.test import TestCase,Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Produit,Commande
from analytics.models import EvenementNavigation
class BoutiqueTests(TestCase):
    def setUp(self):
        self.produit=Produit.objects.create(nom='Test',categorie='telephone',prix=1000,stock=3)
    def test_accueil_et_catalogue(self):
        self.assertEqual(self.client.get('/').status_code,200)
        self.assertContains(self.client.get('/produits/'),'Test')
    def test_panier_post_et_quantite(self):
        self.assertEqual(self.client.get(reverse('ajouter_panier',args=[self.produit.pk])).status_code,405)
        self.client.post(reverse('ajouter_panier',args=[self.produit.pk]))
        self.assertContains(self.client.get('/panier/'),'1000')
        self.client.post(reverse('modifier_panier',args=[self.produit.pk]),{'quantite':2})
        self.assertContains(self.client.get('/panier/'),'2000')
    def test_commande_simulee(self):
        u=User.objects.create_user(username='testuser',password='Password123!')
        self.client.force_login(u)
        self.client.post(reverse('ajouter_panier',args=[self.produit.pk]))
        response=self.client.post('/commander/',{'nom':'Test','telephone':'770000000','adresse':'Dakar'})
        self.assertRedirects(response,'/mes-commandes/')
        self.assertEqual(Commande.objects.count(),1)
        self.produit.refresh_from_db();self.assertEqual(self.produit.stock,2)
    def test_consentement(self):
        self.client.get('/produits/')
        self.assertEqual(EvenementNavigation.objects.count(),0)
        self.client.post('/consentement/',{'choix':'oui'})
        self.client.get('/produits/')
        self.assertEqual(EvenementNavigation.objects.count(),1)
