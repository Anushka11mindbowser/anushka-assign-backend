
from django.db import models

# Create your models here.



class Product(models.Model):
    company = models.CharField(max_length=100)
    product_title = models.CharField(max_length=255)
    product_subtitle = models.CharField(max_length=255)
    product_description = models.CharField(max_length=1000)
    product_code = models.CharField(max_length=15)
    product_price = models.CharField(max_length=5)

class Transaction(models.Model):
    card_number = models.CharField(max_length=15)
    status = models.CharField(max_length=11)
    

