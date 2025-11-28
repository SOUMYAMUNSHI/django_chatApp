from django.urls import path
from . import views

urlpatterns = [
    path('', views.Login_, name="Login"),
    path('signup/', views.Signup, name="Signup"),
    path('logout/', views.Logout, name = "Logout")
]