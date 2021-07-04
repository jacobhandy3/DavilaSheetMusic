from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["first_name","last_name","email","address","city","country","region","postal_code"]
        labels = {
            "first_name":"",
            "last_name":"",
            "email":"",
            "address":"",
            "city":"",
            "country":"",
            "region":"",
            "postal_code":"",
        }