from django.core import mail
from django.test import TestCase
from django.test.client import Client


class HomeViewTest(TestCase):

    def test_home_status_code(self):
        client = Client()
        response = client.get(reversed('core:home'))
        self.assertEqual(response.status_code, 200)
