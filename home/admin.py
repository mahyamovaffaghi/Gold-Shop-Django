from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter
# Register your models here.

class ProductVariantInlines(admin.TabularInline):
    model = Variants
    extra = 2
class ProductGalleryInlines(admin.TabularInline):
    model = ProductGallery
    extra = 2

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'amount', 'discount', 'weight' , 'fee'  )
    inlines = [ProductVariantInlines , ProductGalleryInlines]


class CustomerContactAdmin(admin.ModelAdmin):
    list_display = ['customer_fullName' , 'customer_phoneNumber' , 'is_called' , 'needs_callback' , 'created_at' , 'updated_at']
    list_filter = (
        ('created_at', JDateFieldListFilter),
        ('updated_at', JDateFieldListFilter),
    )
class CaregoryAdmin(admin.ModelAdmin):
    list_display = ('name' , 'slug' , 'sub_category_accessory' , 'is_brand')
    prepopulated_fields = {
        'slug' : ('name' , )
    }
admin.site.register(Category , CaregoryAdmin)
admin.site.register(Product , ProductAdmin)
admin.site.register(SliderHomeGallery)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Variants)
admin.site.register(ProductGallery)
admin.site.register(Comments)
admin.site.register(AdvertisingVideo)
admin.site.register(CustomerContact , CustomerContactAdmin)



