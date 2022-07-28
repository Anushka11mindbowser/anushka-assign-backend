from django import views
from django.urls import path
from cardUser import views

urlpatterns = [
    path('create_card', views.CreateCardUser.as_view(), name="createProfile"),
   
]