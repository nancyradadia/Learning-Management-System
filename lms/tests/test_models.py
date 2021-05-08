from django.test import TestCase

from lms.models import CustomUser,Faculty, Student, Course, Faculty_Course

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


class FacultyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Faculty.objects.create(f_name='Dhaval',l_name='Patel',f_id='AU1841102',email_id='dhaval.p@ahduni.edu.in')

    def test_first_name_label(self):
        author = Faculty.objects.get(email_id='dhaval.p@ahduni.edu.in')
        field_label = author._meta.get_field('f_name').verbose_name
        self.assertEqual(field_label, 'f name')

    def test_string_representation(self):
        entry = Faculty(email_id="dhaval.p@ahduni.edu.in")
        self.assertEqual(str(entry), entry.email_id)

    def test_identification_max_length(self):
        author = Faculty.objects.get(email_id='dhaval.p@ahduni.edu.in')
        max_length = author._meta.get_field('f_id').max_length
        self.assertEqual(max_length, 10)

class StudentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Student.objects.create(f_name='Riya',l_name='Patel',s_id='AU1841102',email_id='riya.p@ahduni.edu.in')

    def test_first_name_label(self):
        author = Student.objects.get(email_id='riya.p@ahduni.edu.in')
        field_label = author._meta.get_field('f_name').verbose_name
        self.assertEqual(field_label, 'f name')

    def test_string_representation(self):
        entry = Student(email_id="riya.p@ahduni.edu.in")
        self.assertEqual(str(entry), entry.email_id)

    def test_identification_max_length(self):
        author = Student.objects.get(email_id='riya.p@ahduni.edu.in')
        max_length = author._meta.get_field('s_id').max_length
        self.assertEqual(max_length, 10)

class Faculty_CourseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        Faculty_Course.objects.create(course_id='CSE450',email='dhaval.p@ahduni.edu.in')

    def test_first_name_label(self):

        author = Faculty_Course.objects.get(email='dhaval.p@ahduni.edu.in')
        field_label = author._meta.get_field('course_id').verbose_name
        self.assertEqual(field_label, 'course id')

    # def test_string_representation(self):
    #     entry = Faculty_Course(email="dhaval.p@ahduni.edu.in")
    #     self.assertEqual(str(entry), entry.email)

    def test_identification_max_length(self):
        author = Faculty_Course.objects.get(email='dhaval.p@ahduni.edu.in')
        max_length = author._meta.get_field('course_id').max_length
        self.assertEqual(max_length, 50)

