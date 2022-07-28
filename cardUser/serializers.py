from dataclasses import fields
from rest_framework import serializers
from .models import CardUser, Product, Transaction

class CardUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CardUser
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

