import datetime
import smtplib

from django.contrib.auth.forms import PasswordChangeForm
import pytz
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Student, Student_Course, CustomUser, Course, Faculty, Faculty_Course, Faculty_Assignment, \
    Student_Assignment, Student_Grade, Resource


def loginPage(request):
    status = None
    if request.user.is_authenticated:
        info = CustomUser.objects.filter(email=request.user)

        for i in info:
            status = i.designation
        if status == 'student':
            return redirect('dashboard')
        else:
            return redirect('faculty_dashboard')

    elif request.method == 'POST':
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = authenticate(request, email=email, password=password)

        if user is not None:
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
    student_info = None
    f_name = None
    s = Student.objects.filter(email_id=request.user)
    for i in s:
        student_info = i.email_id
        f_name = i.f_name

    stu_course_info = Student_Course.objects.filter(email=student_info)
    course = []
    no_of_course = 0
    total_credits = 0
    due_assignments = 0
    for i in stu_course_info:
        cn = Course.objects.filter(course_id=i.course_id)
        total_assignments = Faculty_Assignment.objects.filter(course_id=i.course_id).count()
        completed_assignments = Student_Assignment.objects.filter(course_id=i.course_id,
                                                                  student_id=request.user).count()
        due_assignments = due_assignments + (total_assignments - completed_assignments)

        due = total_assignments - completed_assignments

        for j in cn:
            data = {"course_id": i.course_id,
                    "course_name": j.course_name,
                    "due": due
                    }
            course.append(data)
            no_of_course = no_of_course + 1
            total_credits = total_credits + j.course_credits

    return render(request, 'lms/dashboard.html',
                  context={"name": f_name, "course": course, "no_of_course": no_of_course,
                           "total_credits": total_credits, "due_assignments": due_assignments})


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

        total_assign = Student_Assignment.objects.filter(course_id=i.course_id).count()
        graded_assign = Student_Grade.objects.filter(course_id=i.course_id).count()
        ungraded_assignments = ungraded_assignments + (total_assign - graded_assign)
        due = total_assign - graded_assign

        for j in cn:

            total_stu = Student_Course.objects.filter(course_id=i.course_id).count()
            data = {"course_id": i.course_id,
                    "course_name": j.course_name,
                    "course_count": total_stu,
                    "due": due
                    }
            course.append(data)
            no_of_course = no_of_course + 1

    return render(request, 'lms/faculty_dashboard.html',
                  context={"name": fac_info.f_name, "course": course, "no_of_course": no_of_course,
                           "total_students": no_of_students, "ungraded_assignments": ungraded_assignments})


## view where faculty can view its added assignment, deadline etc..
def faculty_assignment(request,course_name, course_id,assignment_id):

    if (assignment_id!=None):
        Faculty_Assignment.objects.filter(course_id=course_id, assign_id=assignment_id).delete()

    course_info = Faculty_Assignment.objects.filter(course_id=course_id)

    fac_course = Faculty_Course.objects.filter(email=request.user)
    course = []
    designation = "faculty"

    for i in fac_course:

        cn = Course.objects.filter(course_id=i.course_id)

        for j in cn:
            d = {"course_id": i.course_id,
                 "course_name": j.course_name,
                 }
            course.append(d)

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
                  context={"course_id": course_id, "assign_info": assign_info, "course_name": course_name,
                           "course": course, "designation": designation})


## views where faculty can add and edit their assignments
def edit_upload_assignment(request,course_id,course_name,assign_id):

    fac_course = Faculty_Course.objects.filter(email=request.user)
    course = []
    designation = "faculty"

    for i in fac_course:

        cn = Course.objects.filter(course_id=i.course_id)

        for j in cn:
            d = {"course_id": i.course_id,
                 "course_name": j.course_name,
                 }
            course.append(d)

    email = request.user
    faculty = Faculty.objects.get(email_id=email)
    if request.method == 'POST':

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

            if assign_id == "None":

                assig = Faculty_Assignment.objects.filter(course_id=course_id)
                arr = [0]
                for i in assig:
                    a = i.assign_id.split("_", 1)
                    arr.append(int(a[1]))

                id = course_id + '_' + str(max(arr) + 1)
                post.assign_id = id

                post.save()

                text = 'New assignment has been added under course ' + str(course_name)
                subject = 'Check out new assignment on lms'
                email_sender(subject, text, course_id)

            else:


                Faculty_Assignment.objects.filter(assign_id=assign_id).update(PDF=post.PDF, marks=post.marks,
                                                                              deadline=post.deadline)

                text = 'Assignment ' + str(assign_id) + ' has been edited under course ' + str(course_name)
                subject = 'Check out changes in assignment ' + str(assign_id) + 'on lms'
                email_sender(subject, text, course_id)


            s = '/faculty_assignment/' + str(course_id) + '/' + str(course_name) +'/' + 'None'
            return redirect(s)

    return render(request, 'lms/upload.html',
                  context={"course_id": course_id, "course_name": course_name, "course": course,
                           "designation": designation})


## Assignment-Marks-Upload-Resources
def static_page(request, course_name, course_id):

    d = CustomUser.objects.filter(email=request.user)
    designation = None
    for i in d:
        designation = i.designation

    if designation == "faculty":
        fac_course = Faculty_Course.objects.filter(email=request.user)
        course = []
        for i in fac_course:

            cn = Course.objects.filter(course_id=i.course_id)

            for j in cn:
                d = {"course_id": i.course_id,
                     "course_name": j.course_name,
                     }
                course.append(d)

    else:

        e = Student.objects.filter(email_id=request.user)
        email = None
        for i in e:
            email = i.email_id
        stu_course = Student_Course.objects.filter(email=email)
        course = []

        for i in stu_course:

            cn = Course.objects.filter(course_id=i.course_id)

            for j in cn:
                d = {"course_id": i.course_id,
                     "course_name": j.course_name,
                     }
                course.append(d)

    return render(request, 'lms/static.html',
                  context={"course_id": course_id, "designation": designation, "course_name": course_name,
                           "course": course})


## views where student can view the assignments uploaded by repective faculties
def student_assignment(request,course_id,course_name):

    assignments = Faculty_Assignment.objects.filter(course_id=course_id)

    assign_info = []
    deadline = 0

    email = Student.objects.get(email_id=request.user)
    stu_course = Student_Course.objects.filter(email=email)
    course = []
    designation = "student"

    for i in stu_course:

        cn = Course.objects.filter(course_id=i.course_id)

        for j in cn:
            d = {"course_id": i.course_id,
                 "course_name": j.course_name,
                 }
            course.append(d)

    for i in assignments:

        d = Faculty_Assignment.objects.filter(assign_id=i.assign_id)
        for i in d:
            deadline = i.deadline

        count_check = Student_Assignment.objects.filter(assign_id=i.assign_id, student_id=request.user).count()
        if (count_check == 0):
            status = "Upload"

        else:
            graded = Student_Grade.objects.filter(assign_id=i.assign_id, student_id=request.user).count()
            if (graded == 0):
                status = "Edit"
            else:
                status = "View Grades"

        data = {"assign_id": i.assign_id,
                "deadline": deadline,
                "status": status,
                }
        assign_info.append(data)
    return render(request, 'lms/student_assignment.html',
                  context={"assign_info": assign_info, "course_id": course_id, "course_name": course_name,
                           "course": course, "designation": designation})


# Where student can upload or edit assignments
def upload_student_assignment(request,assign_id,course_id,course_name):


    d = Faculty_Assignment.objects.filter(assign_id=assign_id)
    PDF = None
    weightage = None
    email = Student.objects.get(email_id=request.user)
    stu_course = Student_Course.objects.filter(email=email)
    course = []
    designation = "student"

    for i in stu_course:

        cn = Course.objects.filter(course_id=i.course_id)

        for j in cn:
            data = {"course_id": i.course_id,
                    "course_name": j.course_name,
                    }
            course.append(data)

    for i in d:
        deadline = i.deadline
        weightage = i.marks
        PDF = i.PDF

    count_check = Student_Assignment.objects.filter(assign_id=assign_id, student_id=request.user).count()
    if (count_check == 0):
        tz = pytz.timezone('asia/kolkata')
        ct = datetime.datetime.now(tz=tz)

        if (deadline > ct):
            sub = deadline - ct
            string_format = str(sub)
            k = string_format.partition('.')
            diff = k[0] + ' Left for submission'
        else:
            sub = ct - deadline
            string_format = str(sub)
            k = string_format.partition('.')
            diff = k[0] + ' Due for submission'

    else:
        time_of_sub = Student_Assignment.objects.filter(assign_id=assign_id, student_id=request.user)

        for i in time_of_sub:
            submisson = i.time_of_submission

        if deadline > submisson:
            sub = deadline - submisson
            string_format = str(sub)
            k = string_format.partition('.')
            diff = 'Submitted before ' + k[0]
        else:
            sub = submisson - deadline
            string_format = str(sub)
            k = string_format.partition('.')
            diff = 'Submitted after ' + k[0]

    if request.method == 'POST':
        if request.POST:

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
                Student_Assignment.objects.filter(assign_id=assign_id, student_id=request.user).update(PDF=post.PDF,time_of_submission=post.time_of_submission)

            s = '/student_assignment/' + str(course_id) + '/' + str(course_name)
            return redirect(s)

    return render(request, 'lms/student_upload.html',
                  context={"assign_id": assign_id, "course_name": course_name, "weightage": weightage, "PDF": PDF,
                           "status": diff, "deadline": deadline, "designation": designation, "course": course})


## Where faculty gets list of their assignment for grading
def faculty_assignment_list_for_grading(request,course_id,course_name):

    fac_course = Faculty_Course.objects.filter(email=request.user)
    course = []
    designation = "faculty"

    for i in fac_course:

        cn = Course.objects.filter(course_id=i.course_id)

        for j in cn:
            d = {"course_id": i.course_id,
                 "course_name": j.course_name,
                 }
            course.append(d)

    course_info = Faculty_Assignment.objects.filter(course_id=course_id)

    assign_info = []
    for i in course_info:
        a = Student_Grade.objects.filter(assign_id=i.assign_id).count()
        b = Student_Assignment.objects.filter(assign_id=i.assign_id).count()
        if (a == b and a != 0):
            status = "completed"
        elif (a != b):
            status = "Pending"
        else:
            status = "No submissions yet "

        data = {"assign_id": i.assign_id,
                "deadline": i.deadline,
                "status": status
                }
        assign_info.append(data)
    return render(request, 'lms/faculty_assignment_list_for_grading.html',
                  context={"course_id": course_id, "assign_info": assign_info, "course_name": course_name,
                           "course": course, "designation": designation})


# Where faculty can view students submission
def students_submission_list(request,assign_id,course_id,course_name):
    # if request.method == 'GET':
    #     assign_id = request.GET.get('assign_id')
    #     course_name = request.GET.get('course_name')

    fac_course = Faculty_Course.objects.filter(email=request.user)
    course = []
    designation = "faculty"
    for i in fac_course:

        cn = Course.objects.filter(course_id=i.course_id)

        for j in cn:
            d = {"course_id": i.course_id,
                 "course_name": j.course_name,
                 }
            course.append(d)

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
                           "total_submissions": total_submissions, "course_name": course_name, "course": course,
                           "designation": designation})


# where faculty can upload marks of each student
def faculty_grades(request, assign_id, course_id, student_id, course_name):

    fac_course = Faculty_Course.objects.filter(email=request.user)
    course = []
    designation = "faculty"

    for i in fac_course:

        cn = Course.objects.filter(course_id=i.course_id)

        for j in cn:
            d = {"course_id": i.course_id,
                 "course_name": j.course_name,
                 }
            course.append(d)

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
        status = "Submited Late after " + t
    else:
        status_check = deadline - time_of_sub
        string_format = str(status_check)
        k = string_format.partition('.')
        t = k[0]
        status = "Submited before " + t

    if request.method == 'POST':
        if request.POST:

            status_check = Student_Grade.objects.filter(assign_id=assign_id, student_id=student_id).count()

            if (status_check == 0):
                post = Student_Grade()
                post.assign_id = assign_id
                post.course_id = course_id
                post.student_id = student_id
                post.marks = request.POST.get('marks')
                post.comments = request.POST.get('comments')

                post.save()

                email_list = Student_Grade.objects.filter(course_id=course_id)
                addresslist = []
                for i in email_list:
                    email_id = i.student_id
                    e = CustomUser.objects.filter(email=email_id)
                    for j in e:
                        addresslist.append(j.email)

                fromaddr = 'seas.gict@gmail.com'
                for address in addresslist:
                    toaddrs = address
                    text = 'Assignment Garde for ' + str(assign_id) + ' has been added under course ' + str(course_name)
                    subject = 'Check out your grades for ' + str(assign_id) + 'on lms'
                    msg = 'Subject: %s\n\n%s' % (subject, text)
                    username = 'seas.gict@gmail.com'
                    password = 'admin@7016176980'

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(username, password)
                    server.sendmail(fromaddr, toaddrs, msg)
                    server.quit()


            else:

                post = Student_Grade()
                post.marks = request.POST.get('marks')
                post.comments = request.POST.get('comments')

                Student_Grade.objects.filter(assign_id=assign_id, student_id=student_id).update(marks=post.marks,
                                                                                                comments=post.comments)

                email_list = Student_Grade.objects.filter(course_id=course_id)

                addresslist = []
                for i in email_list:
                    email_id = i.student_id
                    e = CustomUser.objects.filter(email=email_id)
                    for j in e:
                        addresslist.append(j.email)

                fromaddr = 'seas.gict@gmail.com'
                for address in addresslist:
                    toaddrs = address
                    text = 'Assignment Garde for ' + str(assign_id) + ' has been reviewed under course ' + str(course_name)
                    subject = 'Check out your reviewed grades for ' + str(assign_id) + 'on lms'
                    msg = 'Subject: %s\n\n%s' % (subject, text)
                    username = 'seas.gict@gmail.com'
                    password = 'admin@7016176980'

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(username, password)
                    server.sendmail(fromaddr, toaddrs, msg)
                    server.quit()

            s = '/students_submission_list/' + str(assign_id) + '/' + str(course_id) + '/' + str(course_name)
            return redirect(s)

    return render(request, 'lms/faculty_grades.html',
                  context={"course_id": course_id, "assign_id": assign_id, "pdf": pdf, "course_name": course_name,
                           "total_marks": total_marks, "status": status, "course": course, "designation": designation})


# students get their grades after evaluation
def get_students_grade(request,course_id,course_name):

    email = Student.objects.get(email_id=request.user)
    stu_course = Student_Course.objects.filter(email=email)
    course = []
    designation = "student"

    for i in stu_course:

        cn = Course.objects.filter(course_id=i.course_id)

        for j in cn:
            d = {"course_id": i.course_id,
                 "course_name": j.course_name,
                 }
            course.append(d)

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

    return render(request, 'lms/students_submission_list.html',
                  context={"course_id": course_id, "graded_assignments": graded_assignments, "course_name": course_name,
                           "course": course, "designation": designation})


#### function to list resources on faculty side
def resources_list(request,course_id,course_name,resource_id):

    if (resource_id):
        Resource.objects.filter(course_id=course_id, resource_id=resource_id).delete()

    res = Resource.objects.filter(course_id=course_id)

    resource_info = []

    for i in res:
        data = {"resource_id": i.resource_id,
                "description": i.description,
                "PDF": i.resource_material}
        resource_info.append(data)

    fac_course = Faculty_Course.objects.filter(email=request.user)
    course = []
    designation = "faculty"
    for i in fac_course:

        cn = Course.objects.filter(course_id=i.course_id)

        for j in cn:
            d = {"course_id": i.course_id,
                 "course_name": j.course_name,
                 }
            course.append(d)

    return render(request, 'lms/resources_list.html',
                  context={"course": course, "designation": designation, "course_name": course_name,
                           "course_id": course_id, "resource_info": resource_info})


def add_resource(request,course_id,course_name,resource_id):


    fac_course = Faculty_Course.objects.filter(email=request.user)
    course = []
    designation = "faculty"

    for i in fac_course:

        cn = Course.objects.filter(course_id=i.course_id)

        for j in cn:
            d = {"course_id": i.course_id,
                 "course_name": j.course_name,
                 }
            course.append(d)


    if request.method == 'POST':
        if request.POST:

            post = Resource()

            post.course_id = course_id
            email = CustomUser.objects.get(email=request.user)
            post.faculty_id = email.email
            post.description = request.POST.get('description')
            file = request.FILES['PDF']
            f = FileSystemStorage()
            fileName = f.save(file.name, file)
            f = 'static/files/' + fileName
            post.resource_material = f

            if (resource_id == "None"):

                res = Resource.objects.filter(course_id=course_id)
                arr = [0]
                for i in res:
                    r = i.resource_id.split("_", 2)
                    arr.append(int(r[2]))

                id = 'R' + '_' + course_id + '_' + str(max(arr) + 1)
                post.resource_id = id
                post.save()
            else:
                Resource.objects.filter(course_id=course_id, resource_id=resource_id).update(
                    description=post.description,
                    resource_material=post.resource_material)
            s = '/resources_list/' + str(course_id) + '/' + str(course_name) + '/None'
            return redirect(s)

    return render(request, 'lms/add_resource.html',
                  context={"course_id": course_id, "course_name": course_name, "course": course,
                           "designation": designation})


### student can view and download resources uploaded by faculty
def download_resources(request,course_id,course_name):

    res = Resource.objects.filter(course_id=course_id)

    resource_info = []

    for i in res:
        data = {"resource_id": i.resource_id,
                "description": i.description,
                "PDF": i.resource_material}
        resource_info.append(data)

    email = Student.objects.get(email_id=request.user)
    stu_course = Student_Course.objects.filter(email=email)
    course = []
    designation = "student"

    for i in stu_course:

        cn = Course.objects.filter(course_id=i.course_id)

        for j in cn:
            d = {"course_id": i.course_id,
                 "course_name": j.course_name,
                 }
            course.append(d)

    return render(request, 'lms/download_resources.html',
                  context={"course_id": course_id, "course_name": course_name, "resource_info": resource_info,
                           "designation": designation, "course": course})


def edit_profile(request):
    d = CustomUser.objects.filter(email=request.user)
    des = None
    f_name = None
    l_name = None
    s_id = None
    for i in d:
        des = i.designation

    if des == "student":

        email = Student.objects.get(email_id=request.user)
        details=Student.objects.filter(email_id=email)
        stu_course = Student_Course.objects.filter(email=email)
        course = []

        for i in stu_course:

            cn = Course.objects.filter(course_id=i.course_id)

            for j in cn:
                d = {"course_id": i.course_id,
                     "course_name": j.course_name,
                     }
                course.append(d)
        for i in details:

                f_name= i.f_name
                l_name= i.l_name
                s_id=i.s_id

    else:
        fac_course = Faculty_Course.objects.filter(email=request.user)
        course = []

        for i in fac_course:

            cn = Course.objects.filter(course_id=i.course_id)

            for j in cn:
                d = {"course_id": i.course_id,
                     "course_name": j.course_name,
                     }
                course.append(d)

    if request.method == 'POST':

        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('logout')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'lms/edit_profile.html', context={"course": course, "form": form, "f_name":f_name,"l_name":l_name,"s_id":s_id})


#### Function to send to email
def email_sender(subject, text, course_id):
    email_list = Student_Course.objects.filter(course_id=course_id)

    addresslist = []
    for i in email_list:
        email_id = i.email
        e = CustomUser.objects.filter(email=email_id)
        for j in e:
            addresslist.append(j.email)

    fromaddr = 'seas.gict@gmail.com'
    for address in addresslist:
        toaddrs = address
        msg = 'Subject: %s\n\n%s' % (subject, text)
        username = 'seas.gict@gmail.com'
        password = 'admin@7016176980'

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()


    return


def enrolled_students(request,course_id,course_name):

    fac_course = Faculty_Course.objects.filter(email=request.user)
    course = []
    designation = "faculty"

    for i in fac_course:

        cn = Course.objects.filter(course_id=i.course_id)

        for j in cn:
            d = {"course_id": i.course_id,
                 "course_name": j.course_name,
                 }
            course.append(d)
    info = []
    e = Student_Course.objects.filter(course_id=course_id)

    for i in e:
        student_info = CustomUser.objects.filter(email=i.email)
        for j in student_info:
            data = {
                "email": i.email,
                "roll": j.identification,
                "first_name": j.first_name,
                "last_name": j.last_name

            }
            info.append(data)

    return render(request, 'lms/enrolled_students.html',
                  context={"course_id": course_id, "info": info, "course_name": course_name, "course": course,
                           "designation": designation})

  # if request.method == 'GET':
    #     course_id = request.GET.get('course_id')
    #     course_name = request.GET.get('course_name')
    # else:
    #     course_id = []
    #     course_name = []