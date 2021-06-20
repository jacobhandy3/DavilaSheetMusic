from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .cart import Cart
from shop.models import SheetMusic
# Create your tests here.

class TestCart(TestCase):
    def setUp(self):
        #create a temporary user to create objects
        self.testUser = User.objects.create(username='JohnDoe',password='DoeTheMan123')
        #setup a factory to generate API requests
        factory = APIRequestFactory()
        #apparently I need to use the session middleware to add a session to requests
        session = SessionMiddleware()
        #test Sheet Music object to go into cart
        SheetMusic.objects.create(
            publisher=self.testUser,
            composer="John Doe",
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            level=3,
            description="Test Description",
            cost=24.99,
            visible=True,
            original=True,
        )
        self.testSheet = SheetMusic.objects.get(title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",level=3,)
        #generate a post request to add item to cart
        request = factory.post(("/cart/create/"+str(self.testSheet.id)))
        #Adding a session to the request
        session.process_request(request)
        request.session.save()
        #Create the cart object and add item to it
        self.cart = Cart(request)
        self.cart.add(self.testSheet,1,False)

    #iteration over all items in the cart
    def test_iter_(self):
        it = 0
        #test Sheet Music object to go into cart
        SheetMusic.objects.create(
            publisher=self.testUser,
            composer="John Doe",
            title="Test Title",
            level=3,
            description="Test Description",
            cost=4.99,
            visible=True,
            original=True,
        )
        #Create another test object to loop twice and add it to cart
        temp = SheetMusic.objects.get(title="Test Title")
        self.cart.add(temp,1,False)
        #loop through cart to test __iter__, increment counter
        for _ in self.cart:
            it += 1
        #verify counter equals number of objects in cart
        self.assertEqual(it,len(self.cart))
    #get total number of items in cart
    def test_len_(self):
        #test Sheet Music object to go into cart
        SheetMusic.objects.create(
            publisher=self.testUser,
            composer="John Doe",
            title="Test Title",
            level=3,
            description="Test Description",
            cost=4.99,
            visible=True,
            original=True,
        )
        temp = SheetMusic.objects.get(title="Test Title")
        self.cart.add(temp,1,False)
        #test there are now 2 objects in cart (first one in setUp and temp one)
        self.assertEqual(len(self.cart),2)
    #add to cart
    def test_add(self):
        #verify the initial test sheet added was indeed added
        self.assertEqual(
            self.cart.cart[str(self.testSheet.id)]["price"],
            str(self.testSheet.cost)
        )
    #calculate the total price of all items in the cart
    def test_get_total_price(self):
        #test Sheet Music object to go into cart
        SheetMusic.objects.create(
            publisher=self.testUser,
            composer="John Doe",
            title="Test Title",
            level=3,
            description="Test Description",
            cost=4.99,
            visible=True,
            original=True,
        )
        temp = SheetMusic.objects.get(title="Test Title")
        #add 2 of the temp sheet just to REALLY test the function
        self.cart.add(temp,2,True)
        #calculate the sum of temp sheet and first sheet costs
        total = (temp.cost * 2) + self.testSheet.cost
        #verify function got the same total
        self.assertEqual(self.cart.get_total_price(),total)
    #remove an item from the cart entirely
    def test_remove(self):
        #test Sheet Music object to go into cart
        SheetMusic.objects.create(
            publisher=self.testUser,
            composer="John Doe",
            title="RIP",
            level=3,
            description="gg...",
            cost=0.99,
            visible=True,
            original=True,
        )
        """Create a sheet music object to be removed and add it to cart"""
        temp = SheetMusic.objects.get(title="RIP")
        self.cart.add(temp,1,False)
        self.assertEqual(
            self.cart.cart[str(temp.id)]["price"],
            str(temp.cost)
        )
        self.cart.remove(temp)
        #Should return None with the dictionary get method
        self.assertIsNone(self.cart.cart.get(str(temp.id)))
    #clear the whole cart and save the new session cookie
    def test_clear(self):
        self.cart.clear()
        #should return none as we deleted this key from session dict
        self.assertIsNone(self.cart.session.get(settings.CART_SESSION_ID))