from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('auth/' , views.auth_view , name='auth_view'),
    path('logout/' , views.logout_user , name='logout_user') ,
    path('profile/', views.profile_view, name='profile_view'),
    path('forget/' , views.forget_password , name='forget_password'),
    path('history/', views.history_view , name='history_view') ,
    path('search/' , views.order_search , name='order_search')

]