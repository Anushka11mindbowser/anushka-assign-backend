from django.db import models
from django.utils import timezone

# Create your models here.


#Model to for products
class Product(models.Model):
    company = models.CharField(max_length=100)
    product_title = models.CharField(max_length=255)
    product_subtitle = models.CharField(max_length=255)
    product_description = models.CharField(max_length=1000)
    product_code = models.CharField(max_length=15)
    product_price = models.CharField(max_length=5)

#Model to store transactions
class Transaction(models.Model):
    customer_name = models.CharField(max_length=255, null=True)
    customer_email = models.CharField(max_length=255,null=True, default="anushkapawar35@gmail.com")
    total_amount = models.IntegerField(null=True)
    payment_method = models.CharField(max_length=255, null=True)
    order_created = models.DateTimeField(default = timezone.now, null=True)
    

