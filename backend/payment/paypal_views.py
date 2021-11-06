from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm

class PaypalProcess:
    def __init__(self, request):
        self.host = request.get_host()
        self.paypalDefaultForm = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": "100",
            "item_name": "Item_Name_xyz",
            "invoice": "Test Payment Invoice",
            "currency_code": "USD",
            "notify_url": "http://{}{}".format(self.host, reverse("paypal-ipn")),
            "return_url": "http://{}{}".format(self.host, reverse("sheetmusic-list")),
            "cancel_return": "http://{}{}".format(self.host, reverse("order-submit")),
        }

    def payment_process(self):
        return PayPalPaymentsForm(initial=self.paypalDefaultForm)
