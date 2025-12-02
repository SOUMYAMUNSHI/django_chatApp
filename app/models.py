from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null= False) #link to user
    chat_msg = models.TextField(max_length=200, null = True, blank= True)
    sender_id = models.TextField(max_length=50)
    receiver_id = models.TextField(max_length=50)
    update_at = models.DateTimeField(auto_now=True)

class chatRoom(models.Model):
    ch_room_name = models.CharField(unique=True, null=False)
    sender_name = models.CharField(null=False)
    receiver_name = models.CharField(null=False)
    first_name = models.TextField(null=False)

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.TextField(max_length=100)
    image = models.ImageField(upload_to="photos/")