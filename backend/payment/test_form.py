from .forms import *
from django.test import TestCase

# Create your tests here.
class OrderFormTest(TestCase):
    def test_form(self):
        form_data = {
            "first_name":"John",
            "last_name":"Doe",
            "email":"doeman123@example.com",
            "address":"145 Sunset St",
            "city":"Fairyland",
            "country":"Neverland",
            "region":"Westlandia",
            "postal_code":"85746",
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())
 