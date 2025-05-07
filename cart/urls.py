from django.urls import path
from . import views

app_name = 'cart'


urlpatterns = [
    path('add/<int:id>/' , views.add_cart , name='add_cart'),
    path('remove/<int:id>/' , views.remove_cart , name='remove_cart') ,
    path('show/' , views.show_cart , name='show_cart') ,
    path('increase/<int:id>/' , views.increase_cart , name='increase_cart') ,
    path('decrease/<int:id>/' , views.decrease_cart , name='decrease_cart')
]