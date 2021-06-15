from shop.models import SheetMusic
from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect, render,get_object_or_404
from django.urls import reverse
from .cart import Cart
from .forms import *
# Create your views here.
def cartDetail(request):
    cart = Cart(request)
    #add current configuration of cart add form for each item in cart (session cookie)
    #to allow reconfiguration (updates) to items in cart page
    for item in cart:
        item['update_quantity_field'] = CartAddForm(initial={'quantity': item['quantity'],'override': True})
    return render(request,"detail.html",{"cart":cart})

def cartCreate(request, id):
    if request.method == "POST":
        cart = Cart(request)
        sheetmusic = get_object_or_404(SheetMusic,id=id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            cart.add(product=sheetmusic,quantity=data["quantity"],override_quantity=data["override"])
        else:
            print(form.errors)
        return redirect(reverse("cart-detail"))
    elif request.method == "GET":
        return redirect(reverse("cart-detail"))
    else:
        return HttpResponseBadRequest("METHOD NOT SUPPORTED!")

def cartDelete(request,id):
    if request.method == "POST":
        cart = Cart(request)
        sheetmusic = get_object_or_404(SheetMusic,id=id)
        cart.remove(sheetmusic)
        return redirect(reverse("cart-detail"))
    elif request.method == "GET":
        return redirect(reverse("cart-detail"))
    else:
        return HttpResponseBadRequest("METHOD NOT SUPPORTED!")