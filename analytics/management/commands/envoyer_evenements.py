import requests
from django.conf import settings
from django.core.management.base import BaseCommand,CommandError
from analytics.models import EvenementNavigation
class Command(BaseCommand):
    help='Transmettre les événements non envoyés à SmartCustomer via API sécurisée.'
    def add_arguments(self,parser): parser.add_argument('--limit',type=int,default=100)
    def handle(self,*args,**options):
        url=settings.SMARTCUSTOMER_API_URL
        token=settings.SMARTCUSTOMER_API_TOKEN
        if not url or not token: raise CommandError('Configurer SMARTCUSTOMER_API_URL et SMARTCUSTOMER_API_TOKEN dans .env')
        if not url.startswith('https://') and not (settings.DEBUG and url.startswith('http://127.0.0.1:')):
            raise CommandError('Une URL HTTPS est nécessaire pour l’API distante.')
        ok=0
        for ev in EvenementNavigation.objects.filter(transmis=False).order_by('id')[:max(1,options['limit'])]:
            payload={'event_id':str(ev.event_id),'session_id':ev.session_id,'user_id':ev.utilisateur_id,'type_evenement':ev.type_evenement,'page':ev.page,'produit_id':ev.produit_id,'commande_id':ev.commande_id,'valeur':str(ev.valeur) if ev.valeur is not None else None,'date_evenement':ev.date_evenement.isoformat()}
            try:
                response=requests.post(url,json=payload,headers={'Authorization':f'Bearer {token}'},timeout=settings.SMARTCUSTOMER_TIMEOUT)
                response.raise_for_status()
                ev.transmis=True;ev.derniere_erreur='';ok+=1
            except requests.RequestException as exc:
                ev.derniere_erreur=str(exc)[:300]
            ev.tentatives+=1
            ev.save(update_fields=['transmis','derniere_erreur','tentatives'])
        self.stdout.write(self.style.SUCCESS(f'{ok} événement(s) transmis.'))
