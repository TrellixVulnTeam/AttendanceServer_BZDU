# view for web
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from First_App.EmailBackEnd import EmailBackEnd
from face_recognition import face_recognition
from .models import Course, Lesson, Attendance, User

def home(request):
    return render(request, 'index.html')
def loginPage(request):

    # user=User.objects.all()
    # print(user)
    # for it in user:
    #
    #     urlknow=it.url_avatar
    #     urlunknown="/media/avatar/16520007.jpg"
    #     known_image = face_recognition.load_image_file(urlknow[1:])
    #     unknown_image = face_recognition.load_image_file(urlunknown[1:])
    #
    #     biden_encoding = face_recognition.face_encodings(known_image)[0]
    #     unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    #     results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
    #     print("len receive: ",results[0])
    #     if(results[0]==True):
    #         print("len receive: ",it.user_name)
    #
    #
    # print("len receive: ", results)
    return render(request, 'login.html')




def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'),
                                         password=request.POST.get('password'))
        # return HttpResponse("<h2>Method  Allowed</h2>")
        if user != None:
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('admin_home')
            # user_type = user.user_type
            # return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
            # if user_type == '1':
            #     return redirect('admin_home')
            #
            # elif user_type == '2':
            #     # return HttpResponse("Staff Login")
            #     return redirect('staff_home')
            #
            # elif user_type == '3':
            #     # return HttpResponse("Student Login")
            #     return redirect('student_home')
            # else:
            #     messages.error(request, "Invalid Login!")
            #     return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            # return HttpResponseRedirect("/")
            return redirect('login')

def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: "+request.user.email+" User Type: "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")



def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/attendance/login/')