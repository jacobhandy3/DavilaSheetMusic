from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from shop.models import SheetMusic

# Create your models here.
class Order(models.Model):
    """Keeps a record of all orders processed"""
    customer = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=75)
    region = models.CharField(max_length=75)
    postal_code = models.CharField(max_length=20)
    created=models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    def get_total_cost(self):
        """Returns total cost of all order items associated with this order id"""
        #items = related name for order item
        return sum(item.get_cost() for item in self.items.all())

    def __str__(self) -> str:
        return "Order %s" % self.id
    class Meta:
        #specify model field to order by
        ordering = ["-created",]
        db_table = "customer_orders"
        #set default name of object
        def __unicode__(self):
            return u"Order %s" % self.id

class OrderItem(models.Model):
    product = models.ForeignKey(SheetMusic,related_name="order_items", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=6,decimal_places=2,validators=[MinValueValidator(limit_value=0,message="Cannot input cost amount lower than $0!")])
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self) -> str:
        return "%s" % self.id
    def get_cost(self):
        """calculates cost of total number of this item"""
        return self.cost * self.quantity
    class Meta:
        #specify model field to order by
        ordering = ["order","quantity","cost"]
        db_table = "order item"
        #set default name of object
        def __unicode__(self):
            return u"%s" % self.id