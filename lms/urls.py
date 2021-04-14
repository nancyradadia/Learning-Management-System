from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('static_page/', views.static_page, name='static_page'),
    path('edit_upload_assignment/', views.edit_upload_assignment, name='edit_upload_assignment'),
    path('faculty_assignment/', views.faculty_assignment, name='faculty_assignment'),
    path('student_assignment/', views.student_assignment, name='student_assignment'),
    path('upload_student_assignment/', views.upload_student_assignment, name='upload_student_assignment'),
    path('faculty_assignment_list_for_grading/', views.faculty_assignment_list_for_grading, name='faculty_assignment_list_for_grading'),
    path('faculty_grades/', views.faculty_grades, name='faculty_grades'),
    path('students_submission_list/', views.students_submission_list, name='students_submission_list'),
    path('get_students_grade/', views.get_students_grade, name='get_students_grade'),
    path('faculty_dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('resources_list/', views.resources_list, name='resources_list'),
    path('add_resource/', views.add_resource, name='add_resource'),
    path('download_resources/', views.download_resources, name='download_resources'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('login/', views.logoutUser, name="logout"),
    path('enrolled_students/', views.enrolled_students, name="enrolled_students"),



]
