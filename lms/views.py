from django.db.models import Count

from .forms import CreateUserForm
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Student, Student_Course, CustomUser, Course, Faculty, Faculty_Course, Faculty_Assignment


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
    no_of_students = []
    for i in fac_course_info:
        cn = Course.objects.filter(course_id=i.course_id)
        total_stu = Student_Course.objects.filter(course_id=i.course_id)
        for j in cn:
            count = 0
            for k in total_stu:
                count = count + 1
            data = {"course_id": i.course_id,
                    "course_name": j.course_name,
                    "course_count": count
                    }
            course.append(data)
            no_of_course = no_of_course + 1
       
    return render(request,'lms/faculty_dashboard.html', 
        context={"name": fac_info.f_name, "course": course, "no_of_course": no_of_course, "total_students": no_of_students})


def faculty_assignment(request):
    if request.method == 'GET':
        course_id = request.GET.get('i.course_id')
        assignment_id = request.GET.get('i.assign_id')
        print(assignment_id)
    else:
        course_id = []
        assignment_id = []
    # course_id = request.GET.get('i.course_id')
    course_info = Faculty_Assignment.objects.filter(course_id=course_id)

    assign_info=[]
    total_assignment=0
    for i in course_info:
        data = {"assign_id": i.assign_id,
                "marks": i.marks,
                "PDF": i.PDF,
                "deadline": i.deadline
                }
        total_assignment = total_assignment+1
        assign_info.append(data)

    return render(request, 'lms/dummy.html',context={"course_id": course_id,"assign_info":assign_info})

def student_assignment(request):

    course_id = request.GET.get('course_id')

    assignments = Faculty_Assignment.objects.filter(course_id=course_id)

    assign_info = []
    total_assignment = 0
    for i in assignments:
        data = {"assign_id": i.assign_id,
                "marks": i.marks,
                "PDF": i.PDF,
                "deadline": i.deadline
                }
        total_assignment = total_assignment + 1
        assign_info.append(data)
        print(assign_info)


    return render(request, 'lms/student_assignment.html',context={"assign_info":assign_info})


def upload_assignment(request):
    if request.method == 'GET':
        course_id = request.GET.get('course_id')
    else:
        course_id = []
    email = request.user
    faculty = Faculty.objects.get(email_id=email)
    if request.method == 'POST':
        course_id = request.GET.get('course_id')

        course_info = Faculty_Assignment.objects.filter(course_id=course_id)
        l = len(course_info)

        if request.POST.get('marks'):
            post = Faculty_Assignment()
            post.marks = request.POST.get('marks')
            post.deadline = request.POST.get('deadline')
            post.faculty_id = faculty.email_id
            post.course_id = course_id
            id = course_id+'_'+str(l+1)
            post.assign_id = id
            file = request.FILES['PDF']
            print(request.FILES)
            f = FileSystemStorage()
            fileName = f.save(file.name, file)
            f = 'static/files/'+fileName
            post.PDF = f
            print(post.course_id)
            print(post.faculty_id)

            post.save()
            print("Data saved")
            s = '/faculty_assignment/?i.course_id='+course_id
            return redirect(s)

    return render(request, 'lms/upload.html',context={"course_id":course_id})


def edit_assignment(request):
    if request.method == 'GET':
        assign_id = request.GET.get('assign_id')

    else:
        assign_id = []

    if request.method == 'POST':
        if request.POST.get('marks'):
            assign_id = request.GET.get('assign_id')
            post = Faculty_Assignment()
            post.marks = request.POST.get('marks')
            post.deadline = request.POST.get('deadline')
            file = request.FILES['PDF']
            print(request.FILES)
            f = FileSystemStorage()
            fileName = f.save(file.name, file)
            f = 'static/files/' + fileName
            post.PDF = f
            print(assign_id)
            Faculty_Assignment.objects.filter(assign_id=assign_id).update(PDF=post.PDF,marks=post.marks,deadline=post.deadline)
            j = assign_id.partition('_')
            course_id = j[0]
            s = '/faculty_assignment/?i.course_id=' + course_id
            return redirect(s)

    return render(request, 'lms/edit.html',context={"assign_id":assign_id})

