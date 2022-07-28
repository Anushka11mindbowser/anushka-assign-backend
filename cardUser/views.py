from django.shortcuts import render
from rest_framework import status
from .models import CardUser
from .serializers import CardUserSerializers
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Create your views here.


# class CreateCardUser(CreateAPIView):
#     serializer_class = CardUserSerializers
#     permission_class = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data= request.data)
#         if serializer.is_valid():
#             serializer.save()
#             response = {
#                 "message":"Card Registered",
#                 "data":serializer.data
#             }

#             return Response(response, status.HTTP_201_CREATED)
#         else:
#             return(serializer.errors, status.HTTP_400_BAD_REQUEST)




class CreateProduct(CreateAPIView):
    model = 