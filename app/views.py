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
    all_chat_users = chatRoom.objects.filter(sender_name = sender_name) | chatRoom.objects.filter(receiver_name = sender_name)
    temp_set1 = set()
    temp_set2 = set()
    for user in all_chat_users:
        temp_set1.add(user.sender_name)
        temp_set2.add(user.receiver_name)

    chat_user = temp_set1.union(temp_set2)

    return render(request, "user/details.html", {'users' : chat_user, 'all_message' : all_message})






@login_required(login_url="Login")
def Profile(request):
    if request.user.is_authenticated:
        current_user = request.user
        print("User id is ......................",current_user.id)
        image = Image.objects.get(user_id = current_user.id)
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
    all_chat_users = chatRoom.objects.filter(sender_name = sender_name) | chatRoom.objects.filter(receiver_name = sender_name)
    temp_set1 = set()
    temp_set2 = set()
    for user in all_chat_users:
        temp_set1.add(user.sender_name)
        temp_set2.add(user.receiver_name)

    chat_user = temp_set1.union(temp_set2)


        


    return render(request, "user/details.html", {'users' : chat_user, 'all_message' : all_message, 'username' : userName,'first_name': sender_first_name, 'send_user_id' : str(sender_user_id), 'current_user':str(current_user_id), 'current_user_name' : current_user_name})
