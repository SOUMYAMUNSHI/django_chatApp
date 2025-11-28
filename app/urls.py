from django.urls import path
from . import views
urlpatterns = [
        path('',views.ChatPage, name="ChatPage"),
        path('/profile/', views.Profile, name = "Profile"),
        path('/search/', views.Search, name = "Search"),
        # path('/<str:userName>', views.newChat, name="newChat" ),
        path('/<str:userName>', views.loadChat, name="loadChat")
]
