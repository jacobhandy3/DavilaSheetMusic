from .forms import *
from django.test import TestCase

# Create your tests here.
class CartAddFormTest(TestCase):
    def test_form(self):
        form = CartAddForm(data={"quantity": 3,"override":True})
        self.assertTrue(form.is_valid())
    def test_num_quantities(self):
        form = CartAddForm()
        self.assertEqual(len(form.fields["quantity"].choices),20)
    def test_override_not_required(self):
        form = CartAddForm(data={"quantity":1})
        self.assertTrue(form.is_valid())
    def test_quantity_required(self):
        form = CartAddForm(data={"override":False})
        self.assertFalse(form.is_valid())