"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

urlpatterns = [
    path(r"admin/", admin.site.urls),
    path(r"paypal/", include("paypal.standard.ipn.urls")),
    path(r"accounts/", include("django.contrib.auth.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path(r"privacy/",TemplateView.as_view(template_name="privacy.html"),name="privacy"),
    path(r"shop/", include("shop.urls"), name="shop"),
    path(r"cart/", include("cart.urls"), name="cart"),
    path(r"order/", include("payment.urls"), name="payment"),
]
