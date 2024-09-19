from django.urls import path
from . import views

app_name = "login"
urlpatterns = [
    path('', views.LoginAndRegister.as_view(), name="LoginAndRegister"),
    path("dangxuat/", views.dangxuat, name="dangxuat"),
]