from statistics import mode
from venv import create
from rest_framework import status
import json
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
product_name = ''



  

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
        # product_id = self.kwargs["pk"]
        # product = Product.objects.get(id=product_id)

        product_name = request.data['product']

        YOUR_DOMAIN = "http://127.0.0.1:8000"

        session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
     line_items=[
                    {
                        'price': 'price_1LSwnKSBTNc3iOhUef9qb5dW',
                        'quantity': 1
                    },
                ],
    mode='payment',
    success_url= YOUR_DOMAIN + '/success/',
    cancel_url= YOUR_DOMAIN + '/cancel/',
  )

        return redirect(session.url, code=303)

       
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, ' whsec_695411eb7f544e31b44527694b06cad3d34402c70c50812264308a4e08d62d84'
        )
    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    except stripe.error.SignatureVerificationError:
        return Response(status=status.HTTP_400_BAD_REQUEST)


    if event[type] == 'checkout.session.completed':
        session =event['data']['object']
        create_order(session)

    return Response(status=status.HTTP_200_OK)


def create_order(session):
    customer_name = session["customer_details"]["name"]
    customer_email = session["customer_details"]["email"]
    order_total = session["amount_data"]
    payment_method = session["payment_method_types"][0]
    str_amount = str(order_total)
    paid_amount = str_amount[:-2]    

    Transaction.objects.create(customer_name=customer_name, customer_email=customer_email, product_name = product_name, total_amount = order_total, payment_method=payment_method, paid_amount=paid_amount)

    


  
        












    



       