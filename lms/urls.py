from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('faculty_dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('faculty_assignment/', views.faculty_assignment, name='faculty_assignment'),
    path('overlay/',views.overlay,name='overlay'),
    path('login/', views.logoutUser, name="logout"),


]