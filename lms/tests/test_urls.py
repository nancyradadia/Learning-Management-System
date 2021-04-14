from django.test import SimpleTestCase
from django.urls import reverse, resolve
from lms.views import dashboard, loginPage, static_page, edit_upload_assignment, faculty_assignment, student_assignment, \
    upload_student_assignment, faculty_assignment_list_for_grading, faculty_grades, students_submission_list, \
    get_students_grade, \
    faculty_dashboard, resources_list, add_resource, download_resources, edit_profile, enrolled_students, logoutUser


class TestUrls(SimpleTestCase):

    def test_login(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, loginPage)

    def test_dashboard(self):
        url = reverse('dashboard')
        self.assertEquals(resolve(url).func, dashboard)

    def test_staticPage(self):
        url = reverse('static_page', args=['course_name', 'course_id'])
        self.assertEquals(resolve(url).func, static_page)

    def test_edit_upload_assignment(self):
        url = reverse('edit_upload_assignment',args=['course_id', 'course_name', 'assign_id'])
        self.assertEquals(resolve(url).func, edit_upload_assignment)

    def test_faculty_assignment(self):
        url = reverse('faculty_assignment',args=['course_id', 'course_name','assignment_id'])
        self.assertEquals(resolve(url).func, faculty_assignment)

    def test_student_assignment(self):
        url = reverse('student_assignment',args=['course_id', 'course_name'])
        self.assertEquals(resolve(url).func, student_assignment)

    def test_upload_student_assignment(self):
        url = reverse('upload_student_assignment',args=['assign_id', 'course_id','course_name'])
        self.assertEquals(resolve(url).func, upload_student_assignment)

    def test_faculty_assignment_list_for_grading(self):
        url = reverse('faculty_assignment_list_for_grading',args=['course_id', 'course_name'])
        self.assertEquals(resolve(url).func, faculty_assignment_list_for_grading)

    # def test_faculty_grades(self):
    #     url = reverse('faculty_grades',args=['assign_id','course_id', 'student_id', 'course_name'])
    #     self.assertEquals(resolve(url).func, faculty_grades)

    def test_students_submission_list(self):
        url = reverse('students_submission_list',args=['assign_id', 'course_id', 'course_name'])
        self.assertEquals(resolve(url).func, students_submission_list)

    def test_get_students_grade(self):
        url = reverse('get_students_grade',args=['course_id', 'course_name'])
        self.assertEquals(resolve(url).func, get_students_grade)

    def test_faculty_dashboard(self):
        url = reverse('faculty_dashboard')
        self.assertEquals(resolve(url).func, faculty_dashboard)

    def test_resources_list(self):
        url = reverse('resources_list',args=['course_id', 'course_name','resource_id'])
        self.assertEquals(resolve(url).func, resources_list)

    def test_add_resource(self):
        url = reverse('add_resource',args=['course_id', 'course_name','resource_id'])
        self.assertEquals(resolve(url).func, add_resource)

    def test_download_resources(self):
        url = reverse('download_resources',args=['course_id', 'course_name'])
        self.assertEquals(resolve(url).func, download_resources)

    def test_edit_profile(self):
        url = reverse('edit_profile')
        self.assertEquals(resolve(url).func, edit_profile)

    def test_enrolled_students(self):
        url = reverse('enrolled_students',args=['course_id', 'course_name'])
        self.assertEquals(resolve(url).func, enrolled_students)

    def test_logoutUser(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logoutUser)

# from django.test import TestCase
# from django.contrib.auth import get_user_model
#
#
# class UsersManagersTests(TestCase):
#
#     def test_create_user(self):
#         User = get_user_model()
#         user = User.objects.create_user(email='normal@user.com', password='foo')
#         self.assertEqual(user.email, 'normal@user.com')
#         self.assertTrue(user.is_active)
#         self.assertFalse(user.is_staff)
#         self.assertFalse(user.is_superuser)
#         try:
#             # username is None for the AbstractUser option
#             # username does not exist for the AbstractBaseUser option
#             self.assertIsNone(user.username)
#         except AttributeError:
#             pass
#         with self.assertRaises(TypeError):
#             User.objects.create_user()
#         with self.assertRaises(TypeError):
#             User.objects.create_user(email='')
#         with self.assertRaises(ValueError):
#             User.objects.create_user(email='', password="foo")
#
#     def test_create_superuser(self):
#         User = get_user_model()
#         admin_user = User.objects.create_superuser('super@user.com', 'foo')
#         self.assertEqual(admin_user.email, 'super@user.com')
#         self.assertTrue(admin_user.is_active)
#         self.assertTrue(admin_user.is_staff)
#         self.assertTrue(admin_user.is_superuser)
#         try:
#             # username is None for the AbstractUser option
#             # username does not exist for the AbstractBaseUser option
#             self.assertIsNone(admin_user.username)
#         except AttributeError:
#             pass
#         with self.assertRaises(ValueError):
#             User.objects.create_superuser(
#                 email='super@user.com', password='foo', is_superuser=False)
#
