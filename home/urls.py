from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug>/<int:id>/', views.all_categories, name='all_categories'),
    path('products/<int:id>/', views.show_products, name='show_products'),
    path('save-search/', views.product_search_save, name='product_search_save'),
    path('all-search/', views.product_search_all, name='product_search_all'),
    path('inner-search/<int:category_id>/', views.product_search_inner, name='product_search_inner') ,
    path('details/<int:id>/', views.product_details, name='product_details'),
    path('save/<int:id>/', views.product_save, name='product_save'),
    path('show-saved-products/', views.show_saved_products, name='show_saved_products'),
    path('like-product/<int:id>/', views.like_product, name='like_product'),
    path('all-products/', views.all_products, name='all_products'),
    path('contact/', views.contact_customer, name='contact_customer'),
    path('comment/<int:id>/', views.product_comment, name='product_comment'),
    path('reply/<int:id_product>/<int:id_comment>', views.comment_reply, name='comment_reply'),
    path('like-comment/<int:id>/', views.like_comment, name='like_comment'),

]
