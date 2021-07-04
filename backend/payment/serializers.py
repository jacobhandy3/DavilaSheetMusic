from rest_framework import serializers
from .models import *

#serializer for model  for JSON conversion for the frontend
class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        #define target model
        model = Order
        #list fields
        fields = ("customer","first_name","last_name","email","address","city","country","region","postal_code")

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        #define target model
        model = OrderItem
        #list fields
        fields = ("product","order","cost","quantity")
        