from backend.exportCSV import export_to_csv
from django.contrib import admin
from .models import *
# Register your models here.

#Admin inline to include in admin form with Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]

# describe model to admin interface
class OrderAdmin(admin.ModelAdmin):
    #list_display lists all the fields in the model
    list_display = ("customer","first_name","last_name","email","address","city","country","region","postal_code")
    #add a section to add order items to order
    inlines = [OrderItemInline]
    #extra actions for the model
    actions = [export_to_csv]

# Register your models here.
admin.site.register(Order, OrderAdmin)
