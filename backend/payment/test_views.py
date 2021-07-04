from rest_framework.test import APIClient,APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import *
from .forms import *

class SheetMusicTests(APITestCase):
    def setUp(self):
        """Create Test Sheet Music Objects"""
        testUser = User.objects.create_user(username="JohnDoe",password="DoeTheMan123",)
        #This will help test that I can see both regular users' orders
        User.objects.create_superuser(username="headhoncho",password="TryMe@69",)

        self.client = APIClient()
        self.testSheet1 = SheetMusic.objects.create(
                publisher=testUser,
                composer="John Doe",
                title="Sheet Music no. 1",
                level=3,
                description="Test Description...",
                cost=4.99,
                visible=True,
                original=True
        )
        self.testSheet2 = SheetMusic.objects.create(
                publisher=testUser,
                composer="Mozart",
                title="Sheet Music no. 9",
                level=5,
                description="Test Description...",
                cost=24.99,
                visible=True,
                original=False
        )

        #Test Order for Order Items
        self.testOrder = Order.objects.create(
            customer=testUser,
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            address="123 Bloomfield Ave",
            city="Summerset",
            country="Neverland",
            region="Cove",
            postal_code="69691",
            paid=True
        )
        #test order items for above order
        OrderItem.objects.create(product=self.testSheet1,order=self.testOrder,cost=self.testSheet1.cost,quantity=2)
        OrderItem.objects.create(product=self.testSheet2,order=self.testOrder,cost=self.testSheet2.cost,quantity=1)
        #Create a new order under guest (no user) to test multiple orders
        second_order = Order.objects.create(
            first_name="Jay",
            last_name="Garcia",
            email="jayman48@example.com",
            address="4567 Minnesota Dr",
            city="New Cairo",
            country="Marsvannia",
            region="Three Wood",
            postal_code="97568",
            paid=True,
        )
        #add order item to guest order
        OrderItem.objects.create(product=self.testSheet2,order=second_order,cost=self.testSheet2.cost,quantity=1)
    
    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="headhoncho",password="TryMe@69")
        #check administrator view of orders
        response = self.client.get("/order/admin/")
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        
        self.client.login(username="JohnDoe",password="DoeTheMan123")
        #check user view of THEIR orders
        response = self.client.get("/order/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/order/submit/")
        self.assertEqual(response.status_code,200)

        response = self.client.post("/order/create/")
        self.assertEqual(response.status_code,200)

    def test_admin_order_list_url_accessible_by_name(self):
        self.client.login(username="headhoncho",password="TryMe@69")
        response = self.client.get(reverse("admin-order-list"))
        self.assertEqual(response.status_code, 200)

    def test_user_order_list_url_accessible_by_name(self):
        self.client.login(username="JohnDoe",password="DoeTheMan123")
        #check user view of THEIR orders
        response = self.client.get(reverse("user-order-list"))
        self.assertEqual(response.status_code, 200)

    def test_get_order_list_url_accessible_by_name(self):
        self.client.login(username="JohnDoe",password="DoeTheMan123")
        #check user view of THEIR orders
        response = self.client.get(reverse("order-submit"))
        self.assertEqual(response.status_code, 200)
    
    def test_order_create_url_accessible_by_name(self):
        self.client.login(username="JohnDoe",password="DoeTheMan123")
        #check user view of THEIR orders
        response = self.client.post(reverse("order-create"))
        self.assertEqual(response.status_code, 200)

    def test_admin_order_list(self):
        self.client.login(username="headhoncho",password="TryMe@69")
        all_orders = Order.objects.all()
        response = self.client.get(reverse("admin-order-list"))
        #Check we got all the orders, should be 2
        self.assertEqual(len(response.data),2)
        self.assertEqual(len(all_orders), len(response.data))
    
    def test_user_order_list(self):
        """Test that the user can only see their orders"""
        testUser = User.objects.get(username="JohnDoe")
        testOrder = Order.objects.create(
            customer=testUser,
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            address="123 Bloomfield Ave",
            city="Summerset",
            country="Neverland",
            region="Cove",
            postal_code="69691",
            paid=True
        )
        OrderItem.objects.create(product=self.testSheet1,order=testOrder,cost=self.testSheet1.cost,quantity=1)
        self.client.login(username="JohnDoe",password="DoeTheMan123")
        user_orders = Order.objects.filter(first_name="John",last_name="Doe")
        response = self.client.get(reverse("user-order-list"))
        #should be length 2
        self.assertEqual(len(response.data),2)
        self.assertEqual(len(user_orders), len(response.data))

    def test_get_order(self):
        """Test form and cart passed through in response"""
        self.client.login(username="JohnDoe",password="DoeTheMan123")
        response = self.client.get(reverse("order-submit"))
        self.assertIsNotNone(response.context.get("form"))
        self.assertIsNotNone(response.context.get("cart"))

    def test_order_create(self):
        """Test order can be created"""
        data = {
            "first_name":"Jake",
            "last_name":"Hager",
            "email":"j.hager@outmail.com",
            "address":"3775 Moonset Ave",
            "city":"Nowhere",
            "country":"United Colonies",
            "region":"New Haven",
            "postal_code":"69786",
        }
        self.client.login(username="JohnDoe",password="DoeTheMan123")
        response = self.client.post(reverse("order-create"),data=data)
        testOrder = Order.objects.filter(first_name="Jake",last_name="Hager").first()
        self.assertEqual(response.status_code,200)
        self.assertIsNotNone(testOrder)
