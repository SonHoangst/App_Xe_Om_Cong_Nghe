from django.urls import path, include
from . import views

app_name = "menu"
urlpatterns = [
    path('', views.showMenu, name="showMenu"),
    path('usermove/', views.userMove.as_view(), name="usermove"),
    path('userfood/', views.userFood.as_view(), name="userfood"),
    path('drivermove/', views.driverMove.as_view(), name="drivermove"),
    path('driverfood/', views.driverFood.as_view(), name="driverfood"),
    path('sellerfood/', views.sellerFood.as_view(), name="sellerfood"),
]