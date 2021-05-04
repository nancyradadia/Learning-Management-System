from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from lms.models import Student, Student_Course, CustomUser, Course, Faculty, Faculty_Course, Faculty_Assignment, \
    Student_Assignment, Student_Grade, Resource


class TestViews(TestCase):


    def test_dashboard_GET(self):
        client = Client()

        response = client.get(reverse('dashboard'))
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed(response, 'lms/dashboard.html')


    def test_static_GET(self):

        client = Client()

        response = client.get(reverse('static_page',args=['course_id','course_name']))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'lms/course_page.html')

    def test_faculty_assignment_GET(self):
        client = Client()

        response = client.get(reverse('faculty_assignment', args=['course_id', 'course_name','assignment_id']))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'lms/course_page.html')
