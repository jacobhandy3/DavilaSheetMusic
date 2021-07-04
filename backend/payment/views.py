from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
# from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from cart.cart import Cart
from .models import *
from .serializers import *
from .forms import *

# Create your views here.
class AdminOrderList(generics.ListAPIView):
    """Displays all orders to admin for various business needs"""
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,IsAdminUser)
    # template_name = "payment/index.html"op
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

class UserOrderList(generics.ListAPIView):
    """Displays users their orders"""
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    # template_name = "payment/index.html"
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.id)

class GetOrder(generics.RetrieveAPIView):
    """Page to get order details"""
    def get(self, request, *args, **kwargs):
        form = OrderForm()
        cart = Cart(request)
        return render(request,"payment/collect_info.html",{"form": form,"cart": cart})
 
class OrderCreate(generics.CreateAPIView):
    """Manages order forms and initiates payment processes"""
    def post(self, request, *args, **kwargs):
        #get the current state of the cart
        cart = Cart(request)
        #verify data is correctly formatted
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save() 
            #create order item objects with items in cart and link them to current order
            for item in cart:
                OrderItem.objects.create(
                    order=order,product=item["product"],price=item["price"],quantity=item["quantity"]
                )
            #clear all items from the cart
            cart.clear()
            #send user to completed page
            return render(request,"payment/order_complete.html",{"order":order})
        #send the user back to the order form with the form errors
        else:
            return render(request,"payment/collect_info.html",{"form": form,"cart": cart, "error":form.errors})
