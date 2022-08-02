from rest_framework import status
from django.shortcuts import redirect
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Product, Transaction
from .serializers import (
                        TransactionSerializer,
                        ProductSerializer
                        )
from rest_framework.generics import (
                                    CreateAPIView, 
                                    GenericAPIView, 
                                    RetrieveAPIView, 
                                    ListAPIView
                                    )



# Create your views here.

stripe.api_key = 'sk_test_51LQVquSBTNc3iOhUdGjqlprwTaOkZ7JCCYpP4KWnPaSv1PNi7ZQPqj4vpYEubGPEKdQydIsIO8woROOOF5LqZ1ed00MO7zYgcU'


class CreateProductView(CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
            "message":"Product Registered",
            "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
class RetrieveProductView(RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = []

    def get_object(self, pk):
        return Product.objects.get(pk=pk)
        

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        product = self.get_object(pk)
        serializer = ProductSerializer(product, many = False)
        response = {
            "message":"Product Retrieved",
            "data":serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
class StripeWebhookView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
            
            'currency': 'inr',
            'product_data': {
            'name': 'Apple Airdopes',
            
            },
            'unit_amount': 2000,
        },
        'quantity': 1,
        }],
        mode='payment',
        success_url='https://example.com/success',
        cancel_url='https://example.com/cancel',
        )

        return Response("Checkout Completed")
       

       
    

class StripeEventListener(CreateAPIView):
    def post(self, request, *args, **kwargs):
        print(request.body)
        return Response(request.body)
    
    


  
        












    



       