from django.contrib import admin
from .models import *
# Register your models here.

class ItemInline(admin.TabularInline) :
    model = ItemOrder
    readonly_fields = ['user' , 'product' , 'variant' , 'quantity']

class OrderAdmin(admin.ModelAdmin) :
    list_display = ('order_user' , 'order_phoneNumber' , 'order_firstName' , 'order_lastName' , 'order_paid' , 'get_price' , 'order_create')
    inlines = [ItemInline]

admin.site.register(Order , OrderAdmin)
admin.site.register(ItemOrder)
admin.site.register(Coupon)
