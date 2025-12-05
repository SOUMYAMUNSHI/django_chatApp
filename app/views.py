from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Chat
from .models import chatRoom
from .models import Image
from django.db.models import Q

# Create your views here.
@login_required(login_url="Login")
def ChatPage(request):
    if request.method == "POST":
        msg = request.POST['msg']
        user = User.objects.get(id = request.user.id)
        sender_id = request.user.id
        receiver_id = 22 #dummy data

        Chat.objects.create(user = user, chat_msg = msg, sender_id = sender_id, receiver_id = receiver_id)

    

    all_message = Chat.objects.all() #fetching all messages

    # all_users = User.objects.values("first_name", "username") #fetching all users
    sender_name = request.user.username

    #fetching all the users based on sender_name and receiver_name
    all_chat_users = chatRoom.objects.filter(sender_name = sender_name) | chatRoom.objects.filter(receiver_name = sender_name)
    #creating two set, to store the unique value
    temp_set1 = set()
    temp_set2 = set()
    #using a for loop to add users in the set
    for user in all_chat_users:
        temp_set1.add(user.sender_name)
        temp_set2.add(user.receiver_name)

    #performing the union() to union the two sets
    chat_user = temp_set1.union(temp_set2)

    #fetchhing the user image based on the perticular user id to show them on chat list section
    images = {}
    for username in chat_user:
        try:
            image = Image.objects.get(user_id = (User.objects.get(username = username).id))
            images[username] = image
        except:
            #using except block to store 'None' if the image is not present for the perticular user
            images[username] = None

    return render(request, "user/details.html", {'users' : chat_user, 'all_message' : all_message, 'user_images' : images.items()})






@login_required(login_url="Login")
def Profile(request):
    if request.user.is_authenticated:
        current_user = request.user
        try:
            image = Image.objects.get(user_id = current_user.id)
        except:
            image = None
    return render(request,"user/profile.html", {'user' : current_user, 'image': image})





login_required(login_url="Login")
def Search(request):
    users = None
    if request.method == "POST":
        search_user = request.POST["user-name"]
        users = User.objects.filter(Q(username__icontains = search_user) | Q(email__icontains = search_user))

    
    return render(request, "user/search.html", {"users" : users})








login_required(login_url="Login")
def loadChat(request, userName):
    sender_user_id = User.objects.get(username = userName).id #fetching user id
    sender_first_name = User.objects.get(username = userName).first_name #fetching first_name
    current_user_id = request.user.id #getting current user id
    current_user_name = User.objects.get(id = current_user_id).username #fetching the username
    all_message = Chat.objects.filter(receiver_id = current_user_id, sender_id = sender_user_id) | Chat.objects.filter(receiver_id = sender_user_id, sender_id = current_user_id) #fetching all messages based on sender_id and receiver_id


    sender_name = request.user.username
    #fetching all the users based on sender_name and receiver_name
    all_chat_users = chatRoom.objects.filter(sender_name = sender_name) | chatRoom.objects.filter(receiver_name = sender_name)
    #creating two set, to store the unique value
    temp_set1 = set()
    temp_set2 = set()
    #using a for loop to add users in the set
    for user in all_chat_users:
        temp_set1.add(user.sender_name)
        temp_set2.add(user.receiver_name)

    #performing the union() to union the two sets
    chat_user = temp_set1.union(temp_set2)

    #fetchhing the user image based on the perticular user id to show them on chat list section
    list_images = {}
    for username in chat_user:
        try:
            list_image = Image.objects.get(user_id = (User.objects.get(username = username).id))
            list_images[username] = list_image
        except:
            list_images[username] = None




    #fetching the user data based on the sender_user_id to show them on perticular chat
    try:
        image = Image.objects.get(user_id = sender_user_id)
    except:
        #using except block to store 'None' if the image is not present for the perticular user
        image = None


    return render(request, "user/details.html", {
        'users' : chat_user, 
        'all_message' : all_message, 
        'username' : userName,
        'first_name': sender_first_name, 
        'send_user_id' : str(sender_user_id), 
        'current_user':str(current_user_id), 
        'current_user_name' : current_user_name, 
        'image': image, 
        'user_images' : list_images.items() #'list_images.items()' create a pair of 'key' and 'vlaues' like this (key, vlaues) which help to access them in template
        })
