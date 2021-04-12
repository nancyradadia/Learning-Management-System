

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
# import django_filters



class Faculty(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    faculty_id = models.CharField(max_length=10,primary_key=True)
    email_id = models.EmailField(max_length=50)

    def __str__(self):
        return self.faculty_id


class Student(models.Model):
    class Meta:
        verbose_name_plural = 'Student Information'

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_id = models.CharField(max_length=10, primary_key=True)
    email_id = models.EmailField(max_length=50)
    admission_year = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.student_id


class Course(models.Model):

    course_id = models.CharField(primary_key=True, max_length=10, null=False)
    course_name = models.CharField(max_length=50, null=False)
    course_details = models.CharField(max_length=500, null=False)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=False)
    course_credits = models.FloatField(null=False)

    class Meta:
        verbose_name_plural = 'Course Information'

    def __str__(self):
        return self.course_id


class Faculty_Course(models.Model):

    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    course_enrollment_year = models.DateField(default=timezone.now)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name_plural = 'Faculty Course Information'

    @property
    def faculty_assignment(self):
        return '{} : {}'.format(self.course_id, self.faculty_id)


class Student_Course(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE,null=False)
    course_enrollment_year = models.DateField(default=timezone.now,null=False)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE,null=False)

    class Meta:
        verbose_name_plural = 'Student Course Information'
        unique_together = (('course_id', 'email', 'course_enrollment_year'),)

    @property
    def faculty_assignment(self):
        return '{} : {}'.format(self.course_id, self.student_id)



class Faculty_Assignment(models.Model):

    assign_id = models.CharField(primary_key=True,max_length=10)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE,null=False)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=False)
    PDF = models.CharField(max_length=50)
    marks = models.IntegerField(null=False)
    deadline = models.DateTimeField()

    def __str__(self):
        return str(self.assign_id)


class Student_Assignment(models.Model):

    assign_id = models.ForeignKey(Faculty_Assignment, on_delete=models.CASCADE,null=False)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE,null=False)
    PDF =  models.CharField(max_length=50)
    time_of_submission = models.DateTimeField()

    def __str__(self):
        return str(self.assign_id)

class Student_Grade(models.Model):

    assign_id = models.ForeignKey(Faculty_Assignment, on_delete=models.CASCADE, null=False)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    comments = models.CharField(max_length=200)
    marks = models.IntegerField()

    def __str__(self):
        return str(self.assign_id)

class Resource(models.Model):

    resource_id = models.CharField(primary_key=True,max_length=10)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE,null=False)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=False)
    resource_material = models.CharField(max_length=50)

    def __str__(self):
        return str(self.resource_id)

