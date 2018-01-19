from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.conf import settings
from simplemooc.simplemooc.courses.models import Courses
from model_mommy import mommy


class ContactManagerTestCase(TestCase):

    def setUp(self):
        self.courses = mommy.make(
            'course.Course', name='Python na web com Django',  _quantity=10
        )
        self.client = Client()

    def tearDown(self):
        for course in self.courses:
            course.delete()

    def test_course_search(self):
        search = Courses.objects.search(object)
        self.assertEqual(len(search), 10)
