from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [

    path('', views.loginPage, name='login'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('faculty_dashboard/', views.faculty_dashboard, name='faculty_dashboard'),

    url(r'^static_page/(?P<course_id>\w+)/(?P<course_name>\w+)/$', views.static_page, name='static_page'),

    url(r'^edit_upload_assignment/(?P<course_id>\w+)/(?P<course_name>\w+)/(?P<assign_id>\w+)/$', views.edit_upload_assignment, name='edit_upload_assignment'),

    url(r'^faculty_assignment/(?P<course_id>\w+)/(?P<course_name>\w+)/(?P<assignment_id>\w+)/$', views.faculty_assignment, name='faculty_assignment'),

    url(r'^faculty_assignment_list_for_grading/(?P<course_id>\w+)/(?P<course_name>\w+)/$', views.faculty_assignment_list_for_grading, name='faculty_assignment_list_for_grading'),

    url(r'^students_submission_list/(?P<assign_id>\w+)/(?P<course_id>\w+)/(?P<course_name>\w+)/$', views.students_submission_list, name='students_submission_list'),

    url(r'^faculty_grades/(?P<assign_id>\w+)/(?P<course_id>\w+)/(?P<student_id>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]+\.[A-Za-z]{2,4})/(?P<course_name>\w+)/$', views.faculty_grades, name='faculty_grades'),

    # url(r'^faculty_grades/(?P<assign_id>\w+)/(?P<course_id>\w+)/(?P<student_id>\w+)/(?P<course_name>\w+)/$', views.faculty_grades, name='faculty_grades'),

    url(r'^resources_list/(?P<course_id>\w+)/(?P<course_name>\w+)/(?P<resource_id>\w+)/$', views.resources_list, name='resources_list'),

    url(r'^add_resource/(?P<course_id>\w+)/(?P<course_name>\w+)/(?P<resource_id>\w+)/$', views.add_resource, name='add_resource'),

    url(r'^enrolled_students/(?P<course_id>\w+)/(?P<course_name>\w+)/$', views.enrolled_students, name='enrolled_students'),

    url(r'^student_assignment/(?P<course_id>\w+)/(?P<course_name>\w+)/$', views.student_assignment, name='student_assignment'),

    url(r'^upload_student_assignment/(?P<assign_id>\w+)/(?P<course_id>\w+)/(?P<course_name>\w+)/$', views.upload_student_assignment, name='upload_student_assignment'),

    url(r'^get_students_grade/(?P<course_id>\w+)/(?P<course_name>\w+)/$', views.get_students_grade, name='get_students_grade'),

    url(r'^download_resources/(?P<course_id>\w+)/(?P<course_name>\w+)/$', views.download_resources, name='download_resources'),

    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('login/', views.logoutUser, name="logout"),



# path('static_page/', views.static_page, name='static_page'),
]
