from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import time
from django.contrib.auth import login, logout, authenticate


# Create your views here.
def Login_(request):
    if request.method == "POST":
        userEmail = request.POST['user-email']
        userPass = request.POST['user-pass']
        try:
            username = User.objects.get(email = userEmail) #fetching the username to authenticate the user
            print("responce", username)
            responce = authenticate(request, username = username, password = userPass)
            login(request, responce) #save the user id in session
            if responce is not None:
                return redirect("ChatPage")
            else:
                return render(request, "login_.html", {"err_msg" : "Crederntials not found"})
        except User.DoesNotExist: #'DoesNotExist' this is an error occurs if email address is not found
            return render(request, "login_.html", {"err_msg" : "Crederntials not found"})

    return render(request, "login_.html")

def Signup(request):
    if request.method == 'POST':
        fstName = request.POST['fst-name']
        print(fstName)
        lstName = request.POST['lst-name']
        print(lstName)
        EmailAddress = request.POST['eml-address']
        print(EmailAddress)
        userName = EmailAddress.split('@')[0] #splitig the first name into 2 string list and taking the starting element as username 
        print(userName)
        password = request.POST['cnf-pswrd']
        print(password)
        # print(userName)
        try:
            if User.objects.filter(email = EmailAddress).exists():
                return render(request, "signup.html", {"err_msg" : "User already exists"})
            
            if User.objects.filter(username = userName).exists():
                uniqueNumber = (str(time.time()).split("."))[1] #taking 5 random number based on current time
                userName += "_" + uniqueNumber[-5:-1] #makig unique username if its already present in DB
                register_flag = User.objects.create_user(username=userName, first_name = fstName, last_name = lstName, email=EmailAddress, password=password)
                if register_flag:
                    return redirect("Login")
                
            else:
                register_flag = User.objects.create_user(username=userName, first_name = fstName, last_name = lstName, email=EmailAddress, password=password)
                if register_flag:
                    return redirect("Login")

        except Exception as e: #to prevent same name conflicts
            print("Use after few seconds", e)
        
    return render(request, "signup.html")

def Logout(request):
    logout(request)
    return redirect("Login")
