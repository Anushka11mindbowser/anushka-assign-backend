from django import views
from django.urls import path

from django import views
from django.urls import path
from cardUser import views



urlpatterns = [
    path('webhook', views.StripeWebhookView.as_view()),
    path('register-product', views.CreateProductView.as_view()),
    path('getProduct/<pk>', views.RetrieveProductView.as_view()),
    path('stripeEventListener', views.StripeEventListener.as_view())
  
    
    
   
]