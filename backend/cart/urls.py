from django.urls import path, reverse
from .views import *

urlpatterns = [
    path("", cartDetail, name="cart-detail"),
    path("create/<int:id>", cartCreate, name="cart-create"),
    path("delete/<int:id>", cartDelete, name="cart-delete"),
]