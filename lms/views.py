import datetime

from django.db.models import Count

from .forms import CreateUserForm
import pytz
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Student, Student_Course, CustomUser, Course, Faculty, Faculty_Course, Faculty_Assignment, \
    Student_Assignment, Student_Grade


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
    due_assignments = 0
    for i in stu_course_info:
        cn = Course.objects.filter(course_id=i.course_id)
        total_assignments = Faculty_Assignment.objects.filter(course_id=i.course_id).count()
        completed_assignments = Student_Assignment.objects.filter(course_id=i.course_id,student_id=request.user).count()
        due_assignments = due_assignments + (total_assignments-completed_assignments)
        print(due_assignments)
        due = total_assignments-completed_assignments

        for j in cn:
            data = {"course_id": i.course_id,
                    "course_name": j.course_name,
                    "due":due
                    }
            course.append(data)
            no_of_course = no_of_course + 1
            total_credits = total_credits + j.course_credits

    return render(request, 'lms/dashboard.html',
                  context={"name": student_info.f_name, "course": course, "no_of_course": no_of_course,
                           "total_credits": total_credits,"due_assignments":due_assignments})


## Faculty dashboard
@login_required(login_url='login')
def faculty_dashboard(request):
    fac_info = Faculty.objects.get(email_id=request.user)
    fac_course_info = Faculty_Course.objects.filter(email=fac_info)
    course = []
    no_of_course = 0
    ungraded_assignments = 0
    no_of_students = []
    for i in fac_course_info:

        cn = Course.objects.filter(course_id=i.course_id)
        total_stu = Student_Course.objects.filter(course_id=i.course_id)

        total_assign = Student_Assignment.objects.filter(course_id=i.course_id).count()
        graded_assign = Student_Grade.objects.filter(course_id=i.course_id).count()
        ungraded_assignments = ungraded_assignments + (total_assign - graded_assign)
        due = total_assign - graded_assign

        for j in cn:
            count = 0
            for k in total_stu:
                count = count + 1
            data = {"course_id": i.course_id,
                    "course_name": j.course_name,
                    "course_count": count,
                    "due": due
                    }
            course.append(data)
            no_of_course = no_of_course + 1

    return render(request, 'lms/faculty_dashboard.html',
                  context={"name": fac_info.f_name, "course": course, "no_of_course": no_of_course,
                           "total_students": no_of_students,"ungraded_assignments":ungraded_assignments})



## view where faculty can view its added assignment, deadline etc..
@login_required(login_url='login')
def faculty_assignment(request):
    if request.method == 'GET':
        course_id = request.GET.get('course_id')
        assignment_id = request.GET.get('i.assign_id')
        course_name = request.GET.get('course_name')

    else:
        course_id = []
        assignment_id = []
        course_name = []

    course_info = Faculty_Assignment.objects.filter(course_id=course_id)

    assign_info = []
    total_assignment = 0
    for i in course_info:
        data = {"assign_id": i.assign_id,
                "marks": i.marks,
                "PDF": i.PDF,
                "deadline": i.deadline
                }
        total_assignment = total_assignment + 1
        assign_info.append(data)

    return render(request, 'lms/faculty_assignments.html',
                  context={"course_id": course_id, "assign_info": assign_info, "course_name": course_name})


## views where faculty can add and edit their assignments
def edit_upload_assignment(request):
    if request.method == 'GET':
        course_id = request.GET.get('course_id')
        course_name = request.GET.get('course_name')
    else:
        course_id = []
        course_name = []
    email = request.user
    faculty = Faculty.objects.get(email_id=email)
    if request.method == 'POST':
        course_id = request.GET.get('course_id')
        course_name = request.GET.get('course_name')
        course_info = Faculty_Assignment.objects.filter(course_id=course_id)
        l = len(course_info)

        if request.POST:
            post = Faculty_Assignment()
            post.marks = request.POST.get('marks')
            post.deadline = request.POST.get('deadline')
            post.faculty_id = faculty.email_id
            post.course_id = course_id

            file = request.FILES['PDF']
            f = FileSystemStorage()
            fileName = f.save(file.name, file)
            f = 'static/files/' + fileName
            post.PDF = f

            assign_id = request.GET.get('assign_id')

            if (assign_id == None):
                id = course_id + '_' + str(l + 1)
                post.assign_id = id

                post.save()

            else:

                Faculty_Assignment.objects.filter(assign_id=assign_id).update(PDF=post.PDF, marks=post.marks,
                                                                              deadline=post.deadline)

            s = '/faculty_assignment/?course_id=' + course_id + '&course_name=' + course_name
            return redirect(s)

    return render(request, 'lms/upload.html', context={"course_id": course_id, "course_name": course_name})


## Assignment-Marks-Upload_Resources
def static_page(request):
    if request.method == 'GET':
        course_id = request.GET.get('course_id')
        course_name = request.GET.get('course_name')
    else:
        course_id = []
        course_name = []

    designation = CustomUser.objects.get(email=request.user)

    return render(request, 'lms/static.html',
                  context={"course_id": course_id, "designation": designation.designation, "course_name": course_name})



## views where student can view the assignments uploaded by repective faculties
def student_assignment(request):
    course_id = request.GET.get('course_id')
    course_name = request.GET.get('course_name')
    assignments = Faculty_Assignment.objects.filter(course_id=course_id)

    assign_info = []
    deadline = 0

    for i in assignments:

        d = Faculty_Assignment.objects.filter(assign_id=i.assign_id)
        for i in d:
            deadline = i.deadline

        count_check = Student_Assignment.objects.filter(assign_id=i.assign_id, student_id=request.user).count()
        if (count_check == 0):
            status = "Upload"

        else:
            graded = Student_Grade.objects.filter(assign_id=i.assign_id,student_id=request.user).count()
            if(graded == 0):
                status = "Edit"
            else:
                print("yes")
                status = "View Grades"

        data = {"assign_id": i.assign_id,
                "deadline": deadline,
                "status": status,
                }
        assign_info.append(data)
    return render(request, 'lms/student_assignment.html',
                  context={"assign_info": assign_info, "course_id": course_id, "course_name": course_name})



# Where student can upload or edit assignments
def upload_student_assignment(request):
    if request.method == 'GET':
        assign_id = request.GET.get('assign_id')
        course_name = request.GET.get('course_name')

        d = Faculty_Assignment.objects.filter(assign_id=assign_id)
        PDF = None

        for i in d:
            deadline = i.deadline
            weightage = i.marks
            PDF = i.PDF


        count_check = Student_Assignment.objects.filter(assign_id=assign_id, student_id=request.user).count()
        if (count_check == 0):
            tz = pytz.timezone('asia/kolkata')
            ct = datetime.datetime.now(tz=tz)

            sub = deadline - ct
            string_format = str(sub)
            k = string_format.partition('.')
            diff = k[0] + ' Left for submission'
        else:
            time_of_sub = Student_Assignment.objects.filter(assign_id=assign_id, student_id=request.user)

            for i in time_of_sub:
                submisson = i.time_of_submission

            sub = deadline - submisson
            string_format = str(sub)
            k = string_format.partition('.')
            diff = 'Submitted before ' + k[0]

    else:
        assign_id = []
        course_name = []



    if request.method == 'POST':
            if request.POST:

                assign_id = request.GET.get('assign_id')

                j = assign_id.partition('_')
                course_id = j[0]

                file = request.FILES['PDF']
                f = FileSystemStorage()
                fileName = f.save(file.name, file)
                f = 'static/files/' + fileName

                status_check = Student_Assignment.objects.filter(assign_id=assign_id, student_id=request.user).count()

                if (status_check == 0):
                    post = Student_Assignment()
                    post.assign_id = assign_id
                    post.course_id = course_id
                    post.student_id = request.user

                    tz = pytz.timezone('asia/kolkata')
                    ct = datetime.datetime.now(tz=tz)

                    post.time_of_submission = ct
                    post.PDF = f

                    post.save()

                else:
                    post = Student_Assignment()
                    post.PDF = f
                    tz = pytz.timezone('asia/kolkata')
                    ct = datetime.datetime.now(tz=tz)

                    post.time_of_submission = ct
                    Student_Assignment.objects.filter(assign_id=assign_id, student_id=request.user).update(PDF=post.PDF,
                                                                                                           time_of_submission=post.time_of_submission)

                s = '/student_assignment/?course_id=' + course_id
                return redirect(s)

    return render(request, 'lms/student_upload.html', context={"assign_id": assign_id,"course_name":course_name,"weightage":weightage,"PDF":PDF,"status":diff,"deadline":deadline})

## Where faculty gets list of their assignment for grading
def faculty_assignment_list_for_grading(request):
    if request.method == 'GET':
        course_id = request.GET.get('course_id')
        course_name = request.GET.get('course_name')

    else:
        course_id = []
        course_name = []

    course_info = Faculty_Assignment.objects.filter(course_id=course_id)

    assign_info = []
    for i in course_info:
        a = Student_Grade.objects.filter(assign_id=i.assign_id).count()
        b = Student_Assignment.objects.filter(assign_id=i.assign_id).count()
        if(a==b and a!=0):
            status = "completed"
        elif(a!=b):
            status = "Pending"
        else:
            status = "No submissions yet "

        data = {"assign_id": i.assign_id,
                "deadline": i.deadline,
                "status": status
                }
        assign_info.append(data)
    return render(request, 'lms/cards.html',
                  context={"course_id": course_id, "assign_info": assign_info, "course_name": course_name})


# Where faculty can view students submission
def students_submission_list(request):
    if request.method == 'GET':
        assign_id = request.GET.get('assign_id')
        course_name = request.GET.get('course_name')

    else:
        assign_id = []
        course_name = []

    j = assign_id.partition('_')
    course_id = j[0]


    deadline = 0
    total_marks = 0
    marks = None



    course_info = Faculty_Assignment.objects.filter(course_id=course_id, assign_id=assign_id)
    for i in course_info:
        deadline = i.deadline
        total_marks = i.marks

    list = Student_Assignment.objects.filter(assign_id=assign_id)

    student_list = []
    total_submissions = 0
    for i in list:
        id = CustomUser.objects.get(email=i.student_id)
        student_grade = Student_Grade.objects.filter(assign_id=assign_id, student_id=i.student_id).count()
        if (student_grade > 0):
            stu = Student_Grade.objects.filter(assign_id=assign_id, student_id=i.student_id)
            for j in stu:
                marks = str(j.marks) + "/" + str(total_marks)
        else:
            marks = "Enter marks"

        if (i.time_of_submission > deadline):
            status_check = i.time_of_submission - deadline
            string_format = str(status_check)
            k = string_format.partition('.')
            t = k[0]
            status = "Late"
        else:
            status_check = deadline - i.time_of_submission
            status = "On Time"
            string_format = str(status_check)
            k = string_format.partition('.')
            t = k[0]

        data = {"assign_id": i.assign_id,
                "student_id": i.student_id,
                "identification": id.identification,
                "status_check": t,
                "status": status,
                "marks": marks
                }
        total_submissions = total_submissions + 1
        student_list.append(data)

    return render(request, 'lms/students_submission_list.html',
                  context={"course_id": course_id, "assign_id": assign_id, "student_list": student_list,
                           "total_submissions": total_submissions,"course_name":course_name})


# where faculty can upload marks of each student
def faculty_grades(request):
    if request.method == 'GET':
        course_id = request.GET.get('course_id')
        assign_id = request.GET.get('assign_id')
        student_id = request.GET.get('student_id')
        course_name = request.GET.get('course_name')
    else:
        course_id = []
        assign_id = []
        student_id = []
        course_name = []

    get_pdf = Student_Assignment.objects.filter(assign_id=assign_id, student_id=student_id)
    time_of_sub = 0
    deadline = 0
    pdf = None
    total_marks = None
    for i in get_pdf:
        pdf = i.PDF
        time_of_sub = i.time_of_submission


    t_m = Faculty_Assignment.objects.filter(assign_id=assign_id)
    for i in t_m:
        total_marks = i.marks
        deadline = i.deadline

    if (time_of_sub > deadline):
        status_check = time_of_sub - deadline
        string_format = str(status_check)
        k = string_format.partition('.')
        t = k[0]
        status = "Submited Late after "+t
    else:
        status_check = deadline - time_of_sub
        string_format = str(status_check)
        k = string_format.partition('.')
        t = k[0]
        status = "Submited before "+t

    if request.method == 'POST':
        if request.POST:

            course_id = request.GET.get('course_id')
            assign_id = request.GET.get('assign_id')
            student_id = request.GET.get('student_id')
            course_name = request.GET.get('course_name')
            status_check = Student_Grade.objects.filter(assign_id=assign_id, student_id=student_id).count()


            if (status_check == 0):
                post = Student_Grade()
                post.assign_id = assign_id
                post.course_id = course_id
                post.student_id = student_id
                post.marks = request.POST.get('marks')
                post.comments = request.POST.get('comments')


                post.save()

            else:

                post = Student_Grade()
                post.marks = request.POST.get('marks')
                post.comments = request.POST.get('comments')


                Student_Grade.objects.filter(assign_id=assign_id, student_id=student_id).update(marks=post.marks,comments=post.comments)

            s = '/students_submission_list/?assign_id=' + assign_id + '&course_name='+course_name
            return redirect(s)

    return render(request, 'lms/faculty_grades.html',
                  context={"course_id": course_id, "assign_id": assign_id, "pdf": pdf,"course_name":course_name,"total_marks":total_marks,"status":status})


# students get their grades afetr evaluation
def get_students_grade(request):
    if request.method == 'GET':
        course_id = request.GET.get('course_id')
        course_name = request.GET.get('course_name')
    else:
        course_id = []
        course_name = []

    marks = None

    list = Student_Grade.objects.filter(course_id=course_id, student_id=request.user)
    graded_assignments = []
    for i in list:
        stu = Faculty_Assignment.objects.filter(assign_id=i.assign_id)
        for j in stu:
            marks = str(i.marks) + "/" + str(j.marks)

        data = {"assign_id": i.assign_id,
                "marks": marks,
                "comments": i.comments}
        graded_assignments.append(data)

    return render(request, 'lms/get_students_grade.html',
                  context={"course_id": course_id, "graded_assignments": graded_assignments,
                           "course_name": course_name})
