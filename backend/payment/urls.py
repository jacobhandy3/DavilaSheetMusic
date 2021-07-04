from django.urls import path, reverse
from .views import *

urlpatterns = [
    path("admin/", AdminOrderList.as_view(), name="admin-order-list"),
    path("", UserOrderList.as_view(), name="user-order-list"),
    path("submit/", GetOrder.as_view(), name="order-submit"),
    path("create/", OrderCreate.as_view(), name="order-create"),
]