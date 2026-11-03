from unittest.mock import Mock, patch

import requests
from django.core.management import call_command
from django.test import TestCase, override_settings

from .models import EvenementNavigation


@override_settings(
    SMARTCUSTOMER_API_URL="https://smartcustomer-analytics.onrender.com/api/smartshop/evenements/",
    SMARTCUSTOMER_API_TOKEN="test-smartshop-token",
    SMARTCUSTOMER_TIMEOUT=8,
)
class SendEventsCommandTests(TestCase):
    def setUp(self):
        self.event = EvenementNavigation.objects.create(
            session_id="session-123",
            type_evenement="product_view",
            page="/produit/1/",
            produit_id=1,
        )

    @patch("analytics.management.commands.envoyer_evenements.requests.post")
    def test_sends_event_with_bearer_token_and_marks_it_transmitted(self, post):
        post.return_value = Mock(status_code=201)

        call_command("envoyer_evenements")

        post.assert_called_once()
        args, kwargs = post.call_args
        self.assertEqual(
            args[0],
            "https://smartcustomer-analytics.onrender.com/api/smartshop/evenements/",
        )
        self.assertEqual(
            kwargs["headers"]["Authorization"],
            "Bearer test-smartshop-token",
        )
        self.assertEqual(kwargs["json"]["event_id"], str(self.event.event_id))
        self.event.refresh_from_db()
        self.assertTrue(self.event.transmis)
        self.assertEqual(self.event.tentatives, 1)

    @patch("analytics.management.commands.envoyer_evenements.requests.post")
    def test_keeps_event_pending_after_http_error(self, post):
        response = Mock(status_code=401)
        response.raise_for_status.side_effect = requests.HTTPError("unauthorized")
        post.return_value = response

        call_command("envoyer_evenements")

        self.event.refresh_from_db()
        self.assertFalse(self.event.transmis)
        self.assertEqual(self.event.tentatives, 1)
        self.assertTrue(self.event.derniere_erreur)
