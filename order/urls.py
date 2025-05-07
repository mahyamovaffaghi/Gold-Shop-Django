from django.urls import path
from . import views

app_name = 'order'


urlpatterns = [
  path('<int:order_id>/' , views.order_show , name='order_show') ,
  path('createOrder/' , views.create_order, name='create_order') ,
  path('coupon/<int:order_id>/' , views.coupon_order , name='coupon_order') ,
  path('paid/<int:order_id>/' , views.paid , name='paid')
]