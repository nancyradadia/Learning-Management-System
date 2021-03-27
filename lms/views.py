from django.db.models import Count

from .forms import CreateUserForm
from django.shortcuts import render, redirect
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Student, Student_Course, CustomUser, Course, Faculty, Faculty_Course


def loginPage(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            messages.info(request, 'Logged in')
            login(request, user)
            info = CustomUser.objects.filter(email=request.user)
            for i in info:
                status = i.designation
            if status == 'student':
                return redirect('dashboard')
            else:
                return redirect('faculty_dashboard')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'lms/login.html', context)


def logoutUser(request):

    logout(request)
    return redirect('login')



@login_required(login_url='login')
def dashboard(request):
    student_info = Student.objects.get(email_id=request.user)
    stu_course_info = Student_Course.objects.filter(email=student_info)
    course = []
    no_of_course = 0
    total_credits = 0
    for i in stu_course_info:
        cn = Course.objects.filter(course_id=i.course_id)
        for j in cn:
            data = {"course_id": i.course_id,
                    "course_name": j.course_name,
                    }
            course.append(data)
            no_of_course = no_of_course + 1
            total_credits = total_credits + j.course_credits

    return render(request, 'lms/dashboard.html',
                  context={"name": student_info.f_name, "course": course, "no_of_course": no_of_course,
                           "total_credits": total_credits})

# Create your views here.
@login_required(login_url='login')
def faculty_dashboard(request):
    fac_info = Faculty.objects.get(email_id=request.user)
    fac_course_info = Faculty_Course.objects.filter(email=fac_info)
    course = []
    no_of_course = 0
    no_of_students = 0
    for i in fac_course_info:
        cn = Course.objects.filter(course_id=i.course_id)
        for j in cn:
            data = {"course_id": i.course_id,
                    "course_name": j.course_name,
                    }
            course.append(data)
            no_of_course = no_of_course + 1
        total_stu = Student_Course.objects.filter(course_id=i.course_id)
        for k in total_stu:
            no_of_students = no_of_students + 1
    return render(request,'lms/faculty_dashboard.html', 
        context={"name": fac_info.f_name, "course": course, "no_of_course": no_of_course, "total_students": no_of_students})

