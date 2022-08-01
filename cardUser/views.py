from distutils.log import error
from tokenize import Token
from django.shortcuts import render
from numpy import generic
from rest_framework import status
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework.generics import (
                                    CreateAPIView, 
                                    GenericAPIView, 
                                    RetrieveAPIView, 
                                    ListAPIView)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Create your views here.


class TransactionLists(CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = []

class StripeWebhookView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        print(request.body)
        return Response("Testing")


  
        












    



       