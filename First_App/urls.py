from django.conf.urls.static import static
from django.urls import path

from UIT_Roll_UP import settings
from . import views, views_web, HodViews

urlpatterns = [
    path('courses/', views.get_courses.as_view()),
    path('attend/', views.image.as_view()),
    path('join/', views.join.as_view()),
    path('register/', views.register.as_view()),
    path('login/', views.login.as_view()),
    path('course/lesson/', views.create_lesson.as_view()),
    # url create lesson with mac address (lap trinh ung dung mang)
    path('course/lesson/location/', views.create_lesson_location.as_view()),
    # url attandance with mac address (lap trinh ung dung mang)
    path('course/lesson/attendance/', views.attendance_location.as_view()),

    path('courses/newcourse/', views.create_new_course.as_view()),
    path('attend/<int:pk>/', views.AttendentDetail.as_view()),
    path('course/lesson/information/', views.infolesson.as_view()),
    path('course/information/', views.infocourse.as_view()),
    path('attend/report/<int:pk>/', views.AttendentReport.as_view()),
    path('information/account/', views.get_inf_account.as_view()),
    path('attend/information/change/<int:pk>/', views.Set_Info_RollUp.as_view()),
    path('user/avatar/change/', views.change_avatar_account.as_view()),
    path('attend/rfid/', views.check_id_rfid.as_view()),
    path('register/rfid/', views.register_card_rfid.as_view()),
    path('account/password/change/', views.change_password.as_view()),
    path('account/password/forgot/', views.forgot_password.as_view()),
    # path('courses/<int:pk>/', views.SnippetDetail.as_view()),

    #     ulr for web
    path('attendance/login/', views_web.loginPage, name="login"),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('attendance/doLogin/', views_web.doLogin, name="doLogin"),
    path('admin_home/', HodViews.admin_home, name="admin_home"),
    path('admin_profile/', HodViews.admin_profile, name="admin_profile"),
    path('logout_user/', views_web.logout_user, name="logout_user"),
    path('manage_student/', HodViews.manage_student, name="manage_student"),
    path('manage_staff/', HodViews.manage_staff, name="manage_staff"),
    path('manage_course/', HodViews.manage_course, name="manage_course"),
    path('manage_lecturer/', HodViews.manage_lecturer, name="manage_lecturer"),
    path('add_student/', HodViews.add_student, name="add_student"),
    path('edit_student/<student_id>', HodViews.edit_student, name="edit_student"),
    path('add_course/', HodViews.add_course, name="add_course"),
    path('edit_course/<course_id>/', HodViews.edit_course, name="edit_course"),
    path('delete_course/<course_id>/', HodViews.delete_course, name="delete_course"),
    path('add_subject/', HodViews.add_subject, name="add_subject"),
    path('add_course_save/', HodViews.add_course_save, name="add_course_save"),
    path('edit_course_save/', HodViews.edit_course_save, name="edit_course_save"),
    path('edit_subject/<lecturer_id>/', HodViews.edit_subject, name="edit_subject"),
    path('delete_subject/<lecturer_id>/', HodViews.delete_subject, name="delete_subject"),
    path('edit_subject_save/', HodViews.edit_subject_save, name="edit_subject_save"),
    path('add_subject_save/', HodViews.add_subject_save, name="add_subject_save"),
    path('delete_student/<student_id>/', HodViews.delete_student, name="delete_student"),
    path('add_student_save/', HodViews.add_student_save, name="add_student_save"),
    path('edit_student_save/', HodViews.edit_student_save, name="edit_student_save"),
    path('admin_profile_update/', HodViews.admin_profile_update, name="admin_profile_update"),
]
