from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.conf import settings
from simplemooc.simplemooc.courses.models import Courses


class ContactCourseTestCase(TestCase):

    def setUp(self):
        self.course = Courses.objects.create(name='Django', slug='django')

    def tearDown(self):
        self.course.delete()

    def test_contact_from_error(self):
        data = {'name': 'Fulano de Tal', 'email': '', 'message': ''}
        client = Client()
        path = reverse('course:details', args=[self.course.slug])
        response = client.post(path, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatorio.')
        self.assertFormError(response, 'form', 'message', 'Este campo é obrigatorio.')

    def test_contact_from_success(self):
        data = {'name': 'Fulano de Tal', 'email': 'admin@adim', 'message': 'oi'}
        client = Client()
        path = reverse('course:details', args=[self.course.slug])
        response = client.post(path, data)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL])
