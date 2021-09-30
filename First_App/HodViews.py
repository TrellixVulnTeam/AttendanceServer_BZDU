import hashlib

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from django.contrib.auth import authenticate, login, logout, get_user, get_user_model
from django.contrib.auth.models import User
from .models import User, Course, Attendance
from .forms import AddStudentForm, EditStudentForm
from django.core.files.storage import FileSystemStorage #To upload Profile Picture

def admin_home(request):
    student = User.objects.filter(user_type='student')
    lecturer = User.objects.filter(user_type='lecturer')
    all_student_count = student.all().count()
    lecturer_count = lecturer.all().count()
    course_count = Course.objects.all().count()
    staff_count = User.objects.all().count()

    # # Total Subjects and students in Each Course
    # course_all = Course.objects.all()
    # course_name_list = []
    # subject_count_list = []
    # student_count_list_in_course = []
    #
    # for course in course_all:
    #     subjects = 1
    #     students = 11
    #     course_name_list.append(course.name)
    #     subject_count_list.append(subjects)
    #     student_count_list_in_course.append(students)
    #
    # subject_all = Course.objects.all()
    # subject_list = []
    # student_count_list_in_subject = []
    # for subject in subject_all:
    #     course = Course.objects.get(code=subject.code)
    #     student_count = 2
    #     subject_list.append(subject.name)
    #     student_count_list_in_subject.append(student_count)

    # # For Saffs
    # staff_attendance_present_list=[]
    # staff_attendance_leave_list=[]
    # staff_name_list=[]
    #
    # staffs = User.objects.all()
    # for staff in staffs:
    #     subject_ids = Subjects.objects.filter(staff_id=staff.admin.id)
    #     attendance = Attendance.objects.filter(subject_id__in=subject_ids).count()
    #     leaves = LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()
    #     staff_attendance_present_list.append(attendance)
    #     staff_attendance_leave_list.append(leaves)
    #     staff_name_list.append(staff.admin.first_name)
    #
    # # For Students
    # student_attendance_present_list=[]
    # student_attendance_leave_list=[]
    # student_name_list=[]
    #
    # students = Students.objects.all()
    # for student in students:
    #     attendance = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
    #     absent = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
    #     leaves = LeaveReportStudent.objects.filter(student_id=student.id, leave_status=1).count()
    #     student_attendance_present_list.append(attendance)
    #     student_attendance_leave_list.append(leaves+absent)
    #     student_name_list.append(student.admin.first_name)
    lecturers = User.objects.filter(user_type='lecturer')
    students=User.objects.filter(user_type='student')
    courses=Course.objects.all()
    context = {
        "all_student_count": all_student_count,
        "lecturer_count": lecturer_count,
        "course_count": course_count,
        "staff_count": staff_count,
        "lecturers": lecturers[0:4],
         "students": students[0:4],
        "courses": courses[0:4]
        # "course_name_list": course_name_list,
        # "subject_count_list": subject_count_list,
        # "student_count_list_in_course": student_count_list_in_course,
        # "subject_list": subject_list,
        # "student_count_list_in_subject": student_count_list_in_subject,
        # "staff_attendance_present_list": staff_attendance_present_list,
        # "staff_attendance_leave_list": staff_attendance_leave_list,
        # "staff_name_list": staff_name_list,
        # "student_attendance_present_list": student_attendance_present_list,
        # "student_attendance_leave_list": student_attendance_leave_list,
        # "student_name_list": student_name_list,
    }
    return render(request, "hod_template/home_content.html", context)


def add_staff(request):
    return render(request, "hod_template/add_staff_template.html")


def add_staff_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_staff')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                  first_name=first_name, last_name=last_name, user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect('add_staff')
        except:
            messages.error(request, "Failed to Add Staff!")
            return redirect('add_staff')


def manage_staff(request):
    staffs = User.objects.all()
    context = {
        "staffs": staffs
    }
    return render(request, "hod_template/manage_staff_template.html", context)


def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)

    context = {
        "staff": staff,
        "id": staff_id
    }
    return render(request, "hod_template/edit_staff_template.html", context)


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get('staff_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            # INSERTING into Staff Model
            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()

            messages.success(request, "Staff Updated Successfully.")
            return redirect('/edit_staff/' + staff_id)

        except:
            messages.error(request, "Failed to Update Staff.")
            return redirect('/edit_staff/' + staff_id)


def delete_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    try:
        staff.delete()
        messages.success(request, "Staff Deleted Successfully.")
        return redirect('manage_staff')
    except:
        messages.error(request, "Failed to Delete Staff.")
        return redirect('manage_staff')


def add_course(request):
    return render(request, "hod_template/add_course_template.html")


def add_course_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_course')
    else:
        code = request.POST.get('coursecode')
        name = request.POST.get('coursename')
        size = request.POST.get('coursesize')
        major = request.POST.get('coursemajor')
        lecturer = request.POST.get('courselecturer')
        lecturercode = request.POST.get('courselecturercode')
        key = request.POST.get('coursekey')
        start_at = request.POST.get('startat')
        end_at = request.POST.get('endat')
        user = User.objects.filter(code_user=lecturercode).first()
        # check if the teacher exists in the database
        if (user == None):
            messages.error(request, "Failed Lecturer code")
            return redirect('add_course')
        else:
            # check lecturer code is true
            if (user.user_type != 'student'):
                course = user.courses.filter(code=code).first()
                # check course code is exists in the database
                if (course != None):
                    messages.error(request, "The course already exists!")
                    return redirect('add_course')
                else:
                    try:
                        user.courses.create(code=code,
                                            name=name,
                                            size=size,
                                            lecturer=lecturer,
                                            code_major=major,
                                            key_course=key,
                                            start=start_at,
                                            end=end_at)
                        messages.success(request, "Course Added Successfully!")
                        return redirect('add_course')
                    except:
                        messages.error(request, "Failed to Add Course!")
                        return redirect('add_course')






def manage_course(request):
    courses = Course.objects.all()
    context = {
        "courses": courses
    }
    return render(request, 'hod_template/manage_course_template.html', context)


def edit_course(request, course_id):
    course = Course.objects.get(id=course_id)
    context = {
        "course": course,
        "id": course_id
    }
    return render(request, 'hod_template/edit_course_template.html', context)


def edit_course_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        course_id = request.POST.get('course_id')
        code = request.POST.get('coursecode')
        name = request.POST.get('coursename')
        size = request.POST.get('coursesize')
        major = request.POST.get('coursemajor')
        lecturer = request.POST.get('courselecturer')
        key = request.POST.get('coursekey')
        start_at = request.POST.get('startat')
        end_at = request.POST.get('endat')

        try:
            course = Course.objects.get(id=course_id)
            course.code = code
            course.name = name
            course.size = size
            course.lecturer = lecturer
            course.code_major = major
            course.key_course = key
            course.start = start_at
            course.end = end_at
            course.save()

            messages.success(request, "Course Updated Successfully.")
            return redirect('/edit_course/' + course_id)

        except:
            messages.error(request, "Failed to Update Course.")
            return redirect('/edit_course/' + course_id)


def delete_course(request, course_id):
    course = Course.objects.get(id=course_id)
    try:
        course.delete()
        messages.success(request, "Course Deleted Successfully.")
        return redirect('manage_course')
    except:
        messages.error(request, "Failed to Delete Course.")
        return redirect('manage_course')


def manage_session(request):
    session_years = SessionYearModel.objects.all()
    context = {
        "session_years": session_years
    }
    return render(request, "hod_template/manage_session_template.html", context)


def add_session(request):
    return render(request, "hod_template/add_session_template.html")


def add_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_course')
    else:
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            sessionyear = SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Session Year added Successfully!")
            return redirect("add_session")
        except:
            messages.error(request, "Failed to Add Session Year")
            return redirect("add_session")


def edit_session(request, session_id):
    session_year = SessionYearModel.objects.get(id=session_id)
    context = {
        "session_year": session_year
    }
    return render(request, "hod_template/edit_session_template.html", context)


def edit_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_session')
    else:
        session_id = request.POST.get('session_id')
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            session_year = SessionYearModel.objects.get(id=session_id)
            session_year.session_start_year = session_start_year
            session_year.session_end_year = session_end_year
            session_year.save()

            messages.success(request, "Session Year Updated Successfully.")
            return redirect('/edit_session/' + session_id)
        except:
            messages.error(request, "Failed to Update Session Year.")
            return redirect('/edit_session/' + session_id)


def delete_session(request, session_id):
    session = SessionYearModel.objects.get(id=session_id)
    try:
        session.delete()
        messages.success(request, "Session Deleted Successfully.")
        return redirect('manage_session')
    except:
        messages.error(request, "Failed to Delete Session.")
        return redirect('manage_session')


def add_student(request):
    return render(request, 'hod_template/add_student_template.html')


def add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_student')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('code')
        name = request.POST.get('name')
        email = request.POST.get('email')
        major = request.POST.get('major')
        type = "student"


        # Upload only if file is selected
        if len(request.FILES) != 0:
            profile_pic = request.FILES['avatar']
            fs = FileSystemStorage()
            # ulr to save image
            path = "avatar/"
            url_save = path + str(code) + ".jpg";
            filename = fs.save(url_save, profile_pic)
            url_avatar = fs.url(filename)
            # print(url_avatar)

        else:
            url_avatar = None
        # hash password for account
        md5 = hashlib.md5(password.encode())
        encryptedPassword = md5.hexdigest()

        # tài khoản đã tồn tại chưa
        user = User.objects.filter(code_user=code).first()
        if (user != None):
            messages.error(request, "Failed to Add Student!")
            return redirect('add_student')
        try:

            student = User(user_name=username,
                           password=encryptedPassword,
                           code_user=code,
                           name=name,
                           email=email,
                           major=major,
                           user_type=type,
                           url_avatar=url_avatar)
            student.save()
            messages.success(request, "Student Added Successfully!")
            return redirect('add_student')
        except:
            messages.error(request, "Failed to Add Student!")
            return redirect('add_student')


def manage_student(request):
    students = User.objects.filter(user_type='student')
    context = {
        "students": students
    }
    return render(request, 'hod_template/manage_student_template.html', context)


def edit_student(request, student_id):
    student = User.objects.get(id=student_id)
    print(student.user_name)
    context = {
        "student": student,
        "id": student_id
    }
    return render(request, "hod_template/edit_student_template.html", context)


def edit_student_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        studentid = request.POST.get('studentid')
        code = request.POST.get('studentcode')
        name = request.POST.get('studentname')
        email = request.POST.get('studentemail')
        major = request.POST.get('studentmajor')

        try:
            student = User.objects.get(id=studentid)
            student.name = name
            student.code_user = code
            student.email = email
            student.major = major

            student.save()

            messages.success(request, "student Updated Successfully.")
            # return redirect('/edit_subject/'+subject_id)
            return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id": studentid}))

        except:
            messages.error(request, "Failed to Update student.")
            return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id": studentid}))
            # return redirect('/edit_subject/'+subject_id)


def delete_student(request, student_id):
    student = User.objects.get(id=student_id)

    try:
        student.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('manage_student')


def add_subject(request):
    return render(request, 'hod_template/add_subject_template.html')


def add_subject_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_subject')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('code')
        name = request.POST.get('name')
        email = request.POST.get('email')
        major = request.POST.get('major')
        type = "lecturer"
        # hash password for account
        md5 = hashlib.md5(password.encode())
        encryptedPassword = md5.hexdigest()

        # Upload only if file is selected
        if len(request.FILES) != 0:
            profile_pic = request.FILES['avatar']
            fs = FileSystemStorage()
            # ulr to save image
            path = "avatar/"
            url_save = path + str(code) + ".jpg";
            filename = fs.save(url_save, profile_pic)
            url_avatar = fs.url(filename)
            # print(url_avatar)

        else:
            url_avatar = None
            # tài khoản đã tồn tại chưa
        user = User.objects.filter(code_user=code).first()
        if (user != None):
            messages.error(request, "Failed to Add Lecturer!")
            return redirect('add_subject')
        try:
            lecturer = User(user_name=username,
                            password=encryptedPassword,
                            code_user=code,
                            name=name,
                            email=email,
                            major=major,
                            user_type=type,
                            url_avatar=url_avatar)
            lecturer.save()
            messages.success(request, "Lecturer Added Successfully!")
            return redirect('add_subject')
        except:
            messages.error(request, "Failed to Add Lecturer!")
            return redirect('add_subject')


def manage_lecturer(request):
    lecturers = User.objects.filter(user_type='lecturer')
    context = {
        "lecturers": lecturers
    }
    return render(request, 'hod_template/manage_subject_template.html', context)


def edit_subject(request, lecturer_id):
    lecturer = User.objects.get(id=lecturer_id)
    print(lecturer.user_name)
    context = {
        "lecturer": lecturer,
        "id": lecturer_id
    }
    # context = {
    #     "subject": subject,
    #     "courses": courses,
    #     "staffs": staffs,
    #     "id": subject_id
    # }
    return render(request, 'hod_template/edit_subject_template.html', context)


def edit_subject_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        lecturerid = request.POST.get('lecturerid')
        code = request.POST.get('Lecturercode')
        name = request.POST.get('lecturername')
        email = request.POST.get('lectureremail')
        major = request.POST.get('lecturermajor')

        try:
            lecturer = User.objects.get(id=lecturerid)
            lecturer.name = name
            lecturer.code_user = code
            lecturer.email = email
            lecturer.major = major

            lecturer.save()

            messages.success(request, "Subject Updated Successfully.")
            # return redirect('/edit_subject/'+subject_id)
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"lecturer_id": lecturerid}))

        except:
            messages.error(request, "Failed to Update Subject.")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"lecturer_id": lecturerid}))
            # return redirect('/edit_subject/'+subject_id)


def delete_subject(request, lecturer_id):
    lecturer = User.objects.get(id=lecturer_id)
    try:
        lecturer.delete()
        messages.success(request, "Subject Deleted Successfully.")
        return redirect('manage_lecturer')
    except:
        messages.error(request, "Failed to Delete Subject.")
        return redirect('manage_lecturer')


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def student_feedback_message(request):
    feedbacks = FeedBackStudent.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/student_feedback_template.html', context)


@csrf_exempt
def student_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def staff_feedback_message(request):
    feedbacks = FeedBackStaffs.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/staff_feedback_template.html', context)


@csrf_exempt
def staff_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/student_leave_view.html', context)


def student_leave_approve(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('student_leave_view')


def student_leave_reject(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('student_leave_view')


def staff_leave_view(request):
    leaves = LeaveReportStaff.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/staff_leave_view.html', context)


def staff_leave_approve(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('staff_leave_view')


def staff_leave_reject(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('staff_leave_view')


def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "hod_template/admin_view_attendance.html", context)


@csrf_exempt
def admin_get_attendance_dates(request):
    # Getting Values from Ajax POST 'Fetch Student'
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year_id")

    # Students enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id
    subject_model = Subjects.objects.get(id=subject_id)

    session_model = SessionYearModel.objects.get(id=session_year)

    # students = Students.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)
    attendance = Attendance.objects.filter(subject_id=subject_model, session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for attendance_single in attendance:
        data_small = {"id": attendance_single.id, "attendance_date": str(attendance_single.attendance_date),
                      "session_year_id": attendance_single.session_year_id.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
    # Getting Values from Ajax POST 'Fetch Student'
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in attendance_data:
        data_small = {"id": student.student_id.admin.id,
                      "name": student.student_id.admin.first_name + " " + student.student_id.admin.last_name,
                      "status": student.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def admin_profile(request):
    user = request.user

    context = {
        "user": user
    }
    return render(request, 'hod_template/admin_profile.html', context)


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = request.user
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')


def staff_profile(request):
    pass


def student_profile(requtest):
    pass

#
#
