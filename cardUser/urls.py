from django import views
from django.urls import path

from django import views
from django.urls import path
from cardUser import views



urlpatterns = [
    path('transaction_list', views.TransactionLists.as_view() ),
    path('webhook', views.StripeWebhookView.as_view())
  
    
    
   
]