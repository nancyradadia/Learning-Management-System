from datetime import timezone, datetime
from time import strftime, gmtime

from django.core.files.storage import FileSystemStorage
from django.db.models import Count

from .forms import CreateUserForm, CreateAssignment
from django.shortcuts import render, redirect
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Student, Student_Course, CustomUser, Course, Faculty, Faculty_Assignment, Faculty_Course


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
    faculty_info = Faculty.objects.get(email_id=request.user)
    faculty_course_info = Faculty_Course.objects.filter(email=faculty_info)
    course = []
    no_of_course = 0
    for i in faculty_course_info:
        cn = Course.objects.filter(course_id=i.course_id)
        for j in cn:
            data = {"course_id": i.course_id,
                    "course_name": j.course_name,
                    }
            course.append(data)
            no_of_course = no_of_course + 1

    return render(request,'lms/faculty_dashboard.html',context={"name": faculty_info.f_name, "course": course, "no_of_course": no_of_course})

def faculty_assignment(request):
    if request.method == 'GET':
        course_id = request.GET.get('i.course_id')

    else:
        course_id = []
    course_info = Faculty_Assignment.objects.filter(course_id=course_id)

    assign_info=[]
    total_assignment=0
    for i in course_info:
        data = {"assign_id": i.assign_id,
                "description": i.description,
                "marks": i.marks,
                "PDF": i.PDF,
                "deadline": i.deadline
                }
        total_assignment = total_assignment+1
        assign_info.append(data)
    # print(assign_info)
    # form = CreateAssignment()
    # if request.method == 'POST':
    #     course_id = request.GET.get('i.course_id')
    #     course_info = Faculty_Assignment.objects.filter(course_id=course_id)
    #     l = len(course_info)
    #     form = CreateAssignment(request.POST)
    #     post = Faculty_Assignment()
    #     post.assign_id = course_id + '_' + str(l + 1)
    #     post.faculty_id = request.user
    #



    if request.method == 'POST':
        course_id = request.GET.get('i.course_id')
        course_info = Faculty_Assignment.objects.filter(course_id=course_id)
        l = len(course_info)
        if request.POST.get('marks') and request.POST.get('description') and request.POST.get('PDF') and request.POST.get('deadline') :
            post = Faculty_Assignment()
            post.marks = request.POST.get('marks')
            post.deadline = request.POST.get('deadline')
            post.description = request.POST.get('description')
            post.faculty_id = request.user
            post.course_id = course_id
            post.assign_id = course_id + '_' + str(l+1)
            post.current_year = strftime("%Y-%m-%d", gmtime())
            post.save()




    return render(request, 'lms/dummy.html',context={"course_id": course_id,"assign_info":assign_info})

def overlay(request):

    return render(request, 'lms/overlay.html')