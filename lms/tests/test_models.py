from django.test import TestCase

from lms.models import CustomUser

class CustomUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        CustomUser.objects.create(email='harvish.j@ahduni.edu.in',identification='AU1841155',first_name='Harvish',last_name='Jariwala')

    def test_first_name_label(self):
        author = CustomUser.objects.get(email='harvish.j@ahduni.edu.in')
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_if_staff_or_not(self):
        author = CustomUser.objects.get(email='harvish.j@ahduni.edu.in')
        field_label = author.is_staff
        self.assertEqual(field_label, False)
        # print("is_staff:",field_label)

    def test_identification_max_length(self):
        author = CustomUser.objects.get(email='harvish.j@ahduni.edu.in')
        max_length = author._meta.get_field('identification').max_length
        self.assertEqual(max_length, 10)