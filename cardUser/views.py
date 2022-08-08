from django.http import HttpResponse
from django.http import HttpRequest
import stripe
from django.conf import settings
from rest_framework import status
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.request import Request
from rest_framework.response import Response

from payment_gateway.settings import WEBHOOK_SECRET_KEY
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

#Stripe Secret Key
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.webhook_key = settings.WEBHOOK_SECRET_KEY
stripe.publishable_key = settings.STRIPE_PUBLISHABLE_KEY    




  
#View To register a product to send it to frontend
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
        
#View to retrieve a product on basis of primary key
class RetrieveProductView(RetrieveAPIView):
    #Mentioning serializer and permission classes
    serializer_class = ProductSerializer
    permission_classes = []

    #Get the specific object on basis of primary key
    def get_object(self, pk):
        return Product.objects.get(pk=pk)
        
    #override the get method to retrieve a particular product
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        product = self.get_object(pk)
        serializer = ProductSerializer(product, many = False)
        response = {
            "message":"Product Retrieved",
            "data":serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


#View to create a checkout_session    
class StripePaymentView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        # product_id = self.kwargs["pk"]
        # product = Product.objects.get(id=product_id)

       
        #Specifying the domain for backend apis
        YOUR_DOMAIN = "http://127.0.0.1:8000"


        #Creating a stripe checkout session
        try:
            session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
        line_items=[
                        {
                            'price': 'price_1LSwnKSBTNc3iOhUef9qb5dW',
                            'quantity': 1
                        },
                    ],
        mode='payment',
        #URLs on for successful payments and canceled payments
        success_url= "http://localhost:4200/success-page?success=true",
        cancel_url= YOUR_DOMAIN + '/cancel/',
    )

            return redirect(session.url, code=303)
        except:
            return Response("Payment Session could not be created", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


#Defining a view for webhooks to listen to stripe events
@csrf_exempt
@api_view(['POST'])
def my_webhook_view(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, stripe.webhook_key
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  

   
  # Handle the checkout.session.completed event
  if event['type'] == 'checkout.session.completed':
    session = event['data']['object']

    # Save an order in your database, marked as 'awaiting payment'
    create_order(session)

    # Check if the order is already paid (for example, from a card payment)
    #
    # A delayed notification payment will have an `unpaid` status, as
    # you're still waiting for funds to be transferred from the customer's
    # account.
    
  elif event['type'] == 'checkout.session.async_payment_succeeded':
    session = event['data']['object']

    
  

 



def create_order(session):
  # TODO: fill me in
    customer_name = session["customer_details"]["name"]
    customer_email = session["customer_details"]["email"]
    order_total = session["amount_total"]
    payment_method = session["payment_method_types"][0]

    transaction = {
        'customer_name' : customer_name,
        'customer_email': customer_email,
        'payment_method':payment_method,
        'order_total':order_total

    }

    serializer = TransactionSerializer(data=transaction)
    if serializer.is_valid():
        serializer.save()
    
    else:
        print(serializer.errors)
        response = {
            'errors':serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # Transaction.objects.create(customer_name=customer_name, customer_email=customer_email, 
    #                             total_amount=order_total, payment_method=payment_method)


     # Passed signature verification
    return HttpResponse(status=200)
