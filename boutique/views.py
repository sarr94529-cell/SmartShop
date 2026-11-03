from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404,redirect,render
from django.views.decorators.http import require_POST
from .forms import InscriptionForm,CommandeForm
from .models import Produit,Commande,LigneCommande
from analytics.services import enregistrer_evenement

def accueil(request):
    enregistrer_evenement(request,'page_view')
    return render(request,'accueil.html',{'produits':Produit.objects.filter(actif=True).order_by('-id')[:8]})

def produits(request):
    enregistrer_evenement(request,'page_view')
    items=Produit.objects.filter(actif=True)
    q=request.GET.get('q','').strip()
    categorie=request.GET.get('categorie','').strip()
    if q: items=items.filter(Q(nom__icontains=q)|Q(description__icontains=q))
    if categorie: items=items.filter(categorie=categorie)
    return render(request,'produits.html',{'produits':items,'q':q,'categorie':categorie,'categories':Produit.CATEGORIES})

def detail_produit(request,pk):
    produit=get_object_or_404(Produit,pk=pk,actif=True)
    enregistrer_evenement(request,'product_view',produit_id=pk)
    return render(request,'detail_produit.html',{'produit':produit})

def lignes_panier(request):
    panier=request.session.get('panier',{})
    articles=[];total=Decimal('0')
    for cle,quantite in panier.items():
        try: produit=Produit.objects.get(pk=int(cle),actif=True)
        except (Produit.DoesNotExist,ValueError,TypeError): continue
        if not isinstance(quantite,int) or quantite<=0: continue
        sous_total=produit.prix*quantite
        articles.append({'produit':produit,'quantite':quantite,'sous_total':sous_total})
        total+=sous_total
    return articles,total

def panier(request):
    articles,total=lignes_panier(request)
    return render(request,'panier.html',{'articles':articles,'total':total})

@require_POST
def ajouter_panier(request,produit_id):
    produit=get_object_or_404(Produit,pk=produit_id,actif=True)
    panier=request.session.get('panier',{})
    cle=str(produit_id)
    if produit.stock<=panier.get(cle,0):
        messages.warning(request,'Stock insuffisant.')
    else:
        panier[cle]=panier.get(cle,0)+1
        request.session['panier']=panier
        enregistrer_evenement(request,'add_to_cart',produit_id=produit_id)
        messages.success(request,'Produit ajouté au panier.')
    return redirect('panier')

@require_POST
def modifier_panier(request,produit_id):
    produit=get_object_or_404(Produit,pk=produit_id)
    panier=request.session.get('panier',{})
    cle=str(produit_id)
    if cle not in panier: return redirect('panier')
    try: quantite=int(request.POST.get('quantite','1'))
    except ValueError: return HttpResponseBadRequest('Quantité invalide')
    if quantite<=0:
        del panier[cle]
        enregistrer_evenement(request,'remove_from_cart',produit_id=produit_id)
    elif quantite<=produit.stock:
        panier[cle]=quantite
        enregistrer_evenement(request,'cart_update',produit_id=produit_id)
    else: messages.error(request,'Quantité supérieure au stock.')
    request.session['panier']=panier
    return redirect('panier')

@require_POST
def supprimer_panier(request,produit_id):
    panier=request.session.get('panier',{})
    if str(produit_id) in panier:
        del panier[str(produit_id)]
        request.session['panier']=panier
        enregistrer_evenement(request,'remove_from_cart',produit_id=produit_id)
    return redirect('panier')

def inscription(request):
    if request.user.is_authenticated: return redirect('accueil')
    form=InscriptionForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        user=form.save();login(request,user);messages.success(request,'Bienvenue sur SmartShop !')
        return redirect('accueil')
    return render(request,'inscription.html',{'form':form})

@login_required
def mes_commandes(request):
    return render(request,'mes_commandes.html',{'commandes':Commande.objects.filter(utilisateur=request.user).order_by('-id')})

@login_required
def commander(request):
    articles,total=lignes_panier(request)
    if not articles:
        messages.warning(request,'Votre panier est vide.')
        return redirect('panier')
    form=CommandeForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        with transaction.atomic():
            produits=[];total_recalcule=Decimal('0')
            for article in articles:
                produit=Produit.objects.select_for_update().get(pk=article['produit'].pk)
                if not produit.actif or produit.stock<article['quantite']:
                    messages.error(request,f'Stock insuffisant pour {produit.nom}.')
                    return redirect('panier')
                produits.append((produit,article['quantite']))
                total_recalcule+=produit.prix*article['quantite']
            commande=Commande.objects.create(utilisateur=request.user,total=total_recalcule,**form.cleaned_data)
            for produit,quantite in produits:
                LigneCommande.objects.create(commande=commande,produit=produit,nom_produit=produit.nom,quantite=quantite,prix_unitaire=produit.prix)
                produit.stock-=quantite;produit.save(update_fields=['stock'])
            request.session['panier']={}
            transaction.on_commit(lambda: enregistrer_evenement(request,'purchase',commande_id=commande.pk,valeur=total_recalcule))
        messages.success(request,'Commande de démonstration confirmée : aucun paiement réel.')
        return redirect('mes_commandes')
    return render(request,'commander.html',{'form':form,'articles':articles,'total':total})

@require_POST
def consentement(request):
    choix=request.POST.get('choix')
    if choix not in ('oui','non'): return HttpResponseBadRequest('Choix invalide')
    request.session['analytics_consent']=(choix=='oui')
    return redirect(request.META.get('HTTP_REFERER','/') if request.META.get('HTTP_REFERER','/').startswith('/') else '/')
