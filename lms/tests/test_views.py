from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:

            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('super@user.com', 'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:

            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)


    def test_static_GET(self):

        client = Client()

        response = client.get(reverse('static_page',args=['course_id','course_name']))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'lms/static.html')


    def test_faculty_assignment_GET(self):

        client = Client()

        response = client.get(reverse('faculty_assignment', args=['course_id', 'course_name','assignment_id']))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'lms/faculty_assignments.html')


    def test_static_page_GET(self):

        client = Client()

        response = client.get(reverse('static_page', args=['course_name', 'course_id']))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'lms/static.html')


    def test_faculty_assignment_list_for_grading_GET(self):

        client = Client()

        response = client.get(reverse('faculty_assignment_list_for_grading', args=['course_id', 'course_name']))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'lms/faculty_assignment_list_for_grading.html')


    def test_students_submission_list_GET(self):
        client = Client()

        response = client.get(reverse('students_submission_list', args=['assign_id', 'course_id', 'course_name']))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'lms/students_submission_list.html')


    def test_resources_list_GET(self):
        client = Client()

        response = client.get(reverse('resources_list', args=['course_id', 'course_name','resource_id']))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'lms/resources_list.html')






