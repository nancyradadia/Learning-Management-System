from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('faculty_assignment/', views.faculty_assignment, name='faculty_assignment'),
    path('static_page/', views.static_page, name='static_page'),
    path('upload_assignment/', views.upload_assignment, name='upload_assignment'),
    path('edit_assignment/', views.edit_assignment, name='edit_assignment'),
    path('student_assignment/', views.student_assignment, name='student_assignment'),
    path('faculty_dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('login/', views.logoutUser, name="logout"),

]
