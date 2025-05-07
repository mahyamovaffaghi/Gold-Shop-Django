from django.db import models
from home.models import *
from django.forms import ModelForm
from django_jalali.db import models as jmodels


# Create your models here.

class Order(models.Model) :
    order_user = models.ForeignKey(User , on_delete=models.CASCADE)
    order_create = jmodels.jDateTimeField(auto_now_add=True)
    order_discount = models.PositiveIntegerField(blank=True , null = True)
    order_paid = models.BooleanField(default=False)
    order_phoneNumber = models.CharField(max_length=12)
    order_firstName = models.CharField(max_length=100)
    order_lastName = models.CharField(max_length=100)
    order_address = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.order_user.phone_number} - {self.order_user.l_name}'

    def get_price(self):
        total = sum(i.price() for i in self.order_item.all())
        if self.order_discount :
            discount_price  = (self.order_discount / 100) * total
            return int(total - discount_price)
        return total

class ItemOrder(models.Model) :
    order = models.ForeignKey(Order , on_delete=models.CASCADE , related_name='order_item')
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants , on_delete=models.CASCADE , null=True , blank=True)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.user.phone_number} - {self.user.l_name}'

    def price(self):
        if self.product.status != 'None' and self.variant:
            return self.variant.total_price * self.quantity
        else:
            return self.product.total_price * self.quantity

class OrderForm(ModelForm) :
    class Meta :
        model = Order
        fields = ['order_phoneNumber' , 'order_firstName' , 'order_lastName' , 'order_address']



class Coupon(models.Model):
    code = models.CharField(max_length=100 , unique=True)
    coupon_active = models.BooleanField(default=False)
    start = jmodels.jDateTimeField()
    end = jmodels.jDateTimeField()
    discount = models.IntegerField()

    def __str__(self):
        return self.code