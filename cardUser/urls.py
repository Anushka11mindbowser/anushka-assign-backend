from django import views
from django.urls import path
from cardUser import views



urlpatterns = [
    path('webhook', views.StripePaymentView.as_view()),
    path('register-product', views.CreateProductView.as_view()),
    path('getProduct/<pk>', views.RetrieveProductView.as_view()),
    
    ]