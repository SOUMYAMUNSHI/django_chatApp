#This is the urls for the django-channel

from django.urls import path
from . import consumers

webSocket_urlspattern = [
    path('ws/sc/<str:username>', consumers.MySyncChannel.as_asgi()),
    # path('ws/ac/<str:username>',consumers.MyAsyncChannel.as_asgi()),
]