from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
# import django_filters


from .managers import CustomUserManager

DESIGNATION_CHOICE = (
    ('student', 'STUDENT'),
    ('faculty', 'FACULTY'),
)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, null=False)
    identification = models.CharField(max_length=10, unique=True, primary_key=True, null=False)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    is_staff = models.BooleanField(default=False, null=False)
    is_active = models.BooleanField(default=True, null=False)
    date_joined = models.DateTimeField(default=timezone.now)
    designation = models.CharField(max_length=7, choices=DESIGNATION_CHOICE, default='student', null=False)

    class Meta:
        unique_together = (('email', 'identification', 'designation'),)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Faculty(models.Model):
    class Meta:
        verbose_name_plural = 'Faculty Information'

    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    f_id = models.CharField(max_length=10)
    email_id = models.EmailField(max_length=50)

    def __str__(self):
        return self.email_id


class Student(models.Model):
    class Meta:
        verbose_name_plural = 'Student Information'


    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    s_id = models.CharField(max_length=10)
    email_id = models.EmailField(primary_key=True,max_length=50)
    admission_year = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email_id
    # user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,default="", editable=False)


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:

        print(instance.designation)
        if instance.designation == 'faculty':
            Faculty.objects.create(email_id=instance.email, f_id=instance.identification,
                                   f_name=instance.first_name, l_name=instance.last_name)
        if instance.designation == 'student':
            Student.objects.create(email_id=instance.email, s_id=instance.identification, f_name=instance.first_name,
                                   l_name=instance.last_name, admission_year=instance.date_joined)


class Course(models.Model):

    course_id = models.CharField(primary_key=True,max_length=10, null=False)
    course_name = models.CharField(max_length=50, null=False)
    course_details = models.CharField(max_length=500, null=False)
    professor_id = models.ForeignKey(Faculty, on_delete=models.CASCADE,null=False)
    course_credits = models.FloatField(null=False)

    class Meta:
        verbose_name_plural = 'Course Information'
        unique_together = (('course_id', 'professor_id', 'course_name'),)

    def __str__(self):
        return self.course_id


class Faculty_Course(models.Model):

    course_id = models.CharField(max_length=50)
    course_enrollment_year = models.DateField(default=timezone.now)
    email = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Faculty Course Information'
        unique_together = (('course_id', 'email', 'course_enrollment_year'),)

    @property
    def faculty_assignment(self):
        return '{} : {}'.format(self.course_id, self.email)


@receiver(post_save, sender=Course)
def create_faculty_profile(sender, instance, created, **kwargs):
    year = timezone.now
    print(instance.course_id)
    print(instance.professor_id)
    Faculty_Course.objects.create(course_id=instance.course_id, course_enrollment_year=year,
                                   email=instance.professor_id)

@receiver(pre_delete, sender=Course)
def delete_faculty_profile(sender, instance, **kwargs):
    Faculty_Course.objects.filter(course_id=instance.course_id).delete()


class Student_Course(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE,null=False)
    course_enrollment_year = models.DateField(default=timezone.now(),null=False)
    email = models.ForeignKey(Student, on_delete=models.CASCADE,null=False)

    class Meta:
        verbose_name_plural = 'Student Course Information'
        unique_together = (('course_id', 'email', 'course_enrollment_year'),)

    def __str__(self):
        return str(self.email)

@receiver(pre_delete, sender=CustomUser)
def delete_profile(sender, instance, **kwargs):
    if instance.designation == 'faculty':
        Faculty.objects.filter(email_id=instance.email).delete()
        Faculty_Course.objects.filter(email=instance.email).delete()

    if instance.designation == 'student':
        Student.objects.filter(email_id=instance.email).delete()
        Student_Course.objects.filter(email=instance.email).delete()

class Faculty_Assignment(models.Model):

    assign_id = models.CharField(primary_key=True,max_length=10)
    course_id = models.CharField(max_length=50)
    faculty_id = models.CharField(max_length=50)
    PDF = models.CharField(max_length=50)
    marks = models.IntegerField(null=False)
    deadline = models.DateTimeField()

    def __str__(self):
        return str(self.course_id)

class Student_Assignment(models.Model):

    assign_id = models.CharField(max_length=10)
    course_id = models.CharField(max_length=50)
    student_id = models.CharField(max_length=50)
    PDF =  models.CharField(max_length=50)
    time_of_submission = models.DateTimeField()

    def __str__(self):
        return str(self.course_id)

class Student_Grade(models.Model):

    assign_id = models.CharField(max_length=10)
    course_id = models.CharField(max_length=50)
    student_id = models.CharField(max_length=50)
    comments = models.CharField(max_length=200)
    marks = models.IntegerField()

    def __str__(self):
        return str(self.assign_id)
