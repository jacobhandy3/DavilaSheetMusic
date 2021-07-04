from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import *

class OrderTestCase(TestCase):
    def setUp(self):
        self.testUser = User.objects.create_user(username='JohnDoe',password='DoeTheMan123')
        self.testSheet1 = SheetMusic.objects.create(
            publisher=self.testUser,
            composer="John Doe",
            title="Songs From The Book of Revelation (Cantata for SATB choir and piano accompaniment)",
            level=3,
            description="Test Description",
            cost=24.99,
            visible=True,
            original=True,
        )
        testSheet2 = SheetMusic.objects.create(
            publisher=self.testUser,
            composer="John Doe",
            title="ii. la llorona (leyendas del valle)",
            level=3,
            description="Test Description",
            cost=5.99,
            visible=False,
            original=False,
        )
        self.testOrder = Order.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            address="123 None Rd",
            city="Nowhere",
            country="Neverland",
            region="Fairy Area",
            postal_code="9999",
            paid=True,
        )
        self.orderItems1 = OrderItem.objects.create(product=self.testSheet1,order=self.testOrder,cost=self.testSheet1.cost,quantity=2)
        self.orderItems2 = OrderItem.objects.create(product=testSheet2,order=self.testOrder,cost=testSheet2.cost,quantity=2)

    def test_total_cost(self):
        total = round((24.99 * 2) + (5.99 * 2),2)
        self.assertEqual(float(self.testOrder.get_total_cost()),total)
    
    def test_get_cost(self):
        self.assertEqual(self.orderItems1.get_cost(),(24.99 * 2))
        self.assertEqual(self.orderItems2.get_cost(),(5.99 * 2))

    def test_min_val_validate(self):
        """Tests that you cannot set an item at a negative value"""
        testOrderItem = OrderItem(product=self.testSheet1,order=self.testOrder,cost=-5,quantity=2)
        try:
            testOrderItem.full_clean()
        except ValidationError as e:
            self.assertEqual("Cannot input cost amount lower than $0!",e.messages[0])
