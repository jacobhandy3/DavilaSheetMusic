from decimal import Decimal
from django.conf import settings
from shop.models import SheetMusic

class Cart:
    """
    class that manages the online cart through sessions
    with all its data and functions.

    Data: sheetmusic instance, quantity, and override quantity
    Functions: add, save, remove, iter, len, get total price, clear
    """
    #Initialize the cart
    def __init__(self,request):
        #store the current session
        self.session = request.session
        #check if a cart exists
        self.cart = self.session.get(settings.CART_SESSION_ID)
        if not self.cart:
            #save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
            self.cart = cart
    #iteration over all items in the cart
    def __iter__(self):
        product_ids = self.cart.keys()
        #queryset of all sheet music objects with ids in cart
        products = SheetMusic.objects.filter(id__in=product_ids)
        #make a copy of the cart
        cart = self.cart.copy()
        #record each object in session cookie
        for p in products:
            cart[str(p.id)]["product"] = p
        #convert price to decimal value for each item in cart
        #and add calculation of total price based on quantity of item requested
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            #return a generator(iterable object) with product, price, and total price
            #which will provide easy acces in views and templates
            yield item
    #get total number of items in cart
    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())
    #save the currrent session with new info
    def save(self):
        self.session.modified = True
    #add to cart
    def add(self,product,quantity=1,override_quantity=False):
        product_id = str(product.id)
        #if new item added to cart, initialize new item in session cookie
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity":0,"price":str(product.cost)}
        #if specific quantity of item passed, set the quantity of item in cart
        if override_quantity == True:
            self.cart[product_id]["quantity"] = quantity
        #otherwise, just add 1 to quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        #save the new information to cart
        self.save()
    #remove an item from the cart entirely
    def remove(self,product):
        product_id = str(product.id)
        #check if item exists in cart, then remove it and save the session
        if product_id in self.cart:
            if self.cart[product_id]["quantity"] == 1:
                del self.cart[product_id]
            else:
                self.cart[product_id]["quantity"] -= 1
            self.save()
    #clear the whole cart and save the new session cookie
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
    #calculate the total price of all items in the cart
    def get_total_price(self):
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())