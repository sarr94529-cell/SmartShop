from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from analytics.delivery import transmettre_evenement
from analytics.models import EvenementNavigation


class Command(BaseCommand):
    help = "Réessayer la transmission des événements SmartCustomer en attente."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=100)

    def handle(self, *args, **options):
        url = settings.SMARTCUSTOMER_API_URL
        token = settings.SMARTCUSTOMER_API_TOKEN
        if not url or not token:
            raise CommandError(
                "Configurer SMARTCUSTOMER_API_URL et SMARTCUSTOMER_API_TOKEN."
            )
        if not url.startswith("https://") and not (
            settings.DEBUG and url.startswith("http://127.0.0.1:")
        ):
            raise CommandError("Une URL HTTPS est nécessaire pour l'API distante.")

        sent = 0
        failed = 0
        events = EvenementNavigation.objects.filter(transmis=False).order_by("id")
        for event in events[: max(1, options["limit"])]:
            if transmettre_evenement(event):
                sent += 1
            else:
                failed += 1

        self.stdout.write(self.style.SUCCESS(f"{sent} événement(s) transmis."))
        if failed:
            self.stderr.write(
                self.style.WARNING(
                    f"{failed} événement(s) restent à transmettre ; "
                    "consultez les journaux et relancez la commande."
                )
            )
