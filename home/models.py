from django.db import models
from django.urls import reverse
from django.forms import ModelForm
from accounts.models import *
from django.forms import ModelForm
from taggit.managers import TaggableManager
from django_jalali.db import models as jmodels
from django.db.models import Avg


# Create your models here.


class Category(models.Model):
    category_accessory = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'  # اضافه کردن related_name
    )
    category_brand = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='brand_subcategories'  # اضافه کردن related_name
    )
    sub_category_accessory = models.BooleanField(default=False)
    is_brand = models.BooleanField(default=False)
    name = models.CharField(max_length=30)
    create_time = jmodels.jDateTimeField(auto_now_add=True)
    update_time = jmodels.jDateTimeField(auto_now=True)
    cat_img = models.ImageField(upload_to='Category', null=True, blank=True)
    cat_video = models.FileField(upload_to='videos', null=True, blank=True)
    slug = models.SlugField(allow_unicode=True, unique=True, null=True, blank=True)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('home:all_categories', args=[self.slug, self.id])


class SliderHomeGallery(models.Model):
    slider_img = models.ImageField(upload_to='Slider', null=True, blank=True)
    slider_title = models.CharField(max_length=300, null=True, blank=True)
    slider_text = models.CharField(max_length=500, null=True, blank=True)


class Product(models.Model):
    VARIANT = (
        ('None', 'هیج کدام'),
        ('Size', 'سایز'),
        ('Color', 'رنگ')
    )
    category = models.ManyToManyField(Category, blank=True)
    product_name = models.CharField(max_length=50)
    amount = models.PositiveSmallIntegerField()
    discount = models.PositiveSmallIntegerField(null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    create_time = jmodels.jDateTimeField(auto_now_add=True)
    update_time = jmodels.jDateTimeField(auto_now=True)
    product_img = models.ImageField(upload_to='Product', null=True, blank=True)
    weight = models.IntegerField()
    fee = models.IntegerField()
    saved_by_users = models.ManyToManyField(User, blank=True, related_name='save_product_user')
    like = models.ManyToManyField(User, blank=True, related_name='product_like')
    # total_price = models.PositiveIntegerField(null=True , blank=True)
    unit_price = models.IntegerField(null=True, blank=True)
    # ojrat,sood,maliat ,totalprice
    status = models.CharField(choices=VARIANT, null=True, blank=True, max_length=5)
    sell = models.PositiveSmallIntegerField(default=0)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.product_name

    @property
    def total_price(self):
        if self.unit_price is None:
            return 0
        if not self.discount:
            return self.unit_price
        total = (self.discount * self.unit_price) / 100
        return int(self.unit_price - total)

    @property
    def average(self):
        data = Comments.objects.filter(is_reply=False, product=self).aggregate(a=Avg('rate'))
        star = 0
        if data['a'] is not None:
            star = round(data['a'], 1)
        return star


class Size(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class Variants(models.Model):
    name = models.CharField(max_length=70)
    product_variant = models.ForeignKey(Product, on_delete=models.CASCADE)
    size_variant = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True)
    color_variant = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)

    amount = models.PositiveSmallIntegerField()
    discount = models.PositiveSmallIntegerField(null=True, blank=True)
    unit_price = models.IntegerField(null=True, blank=True)
    # total_price = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if self.unit_price is None:
            return 0
        if not self.discount:
            return self.unit_price
        total = (self.discount * self.unit_price) / 100
        return int(self.unit_price - total)


class ProductGallery(models.Model):
    product_gallery = models.ForeignKey('Product', on_delete=models.CASCADE)
    gallery_img = models.ImageField(upload_to='Product', null=True, blank=True)


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    rate = models.PositiveIntegerField(default=1)
    create = jmodels.jDateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='comment_reply')
    is_reply = models.BooleanField(default=False)
    comment_like = models.ManyToManyField(User, blank=True, related_name='com_like')

    def __str__(self):
        return self.product.product_name

    def get_absolute_url(self):
        return reverse('home:comment_reply', kwargs={'id_product': self.product.id, 'id_comment': self.id})




class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['comment', 'rate']





class AdvertisingVideo(models.Model):
    advertising_video = models.FileField(upload_to='videos', null=True, blank=True)
    advertising_title = models.CharField(max_length=50, null=True, blank=True)
    advertising_text = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.advertising_title


class CustomerContact(models.Model):
    CALL_STATUS = (
        ('CALLED', 'تماس گرفته شده'),
        ('NOT_CALLED', 'هنوز تماس گرفته نشده'),
    )
    FOLLOW_UP_CALL_NEED = (
        ('NEEDED', 'نیاز به تماس مجدد'),
        ('NOT_NEEDED', 'عدم نیاز به تماس مجدد'),
    )
    created_at = jmodels.jDateTimeField(auto_now_add=True , blank=True , null=True)
    updated_at = jmodels.jDateTimeField(auto_now=True , blank=True , null=True)
    customer_fullName = models.CharField(max_length=120)
    customer_phoneNumber = models.CharField(max_length=12)
    is_called = models.CharField(choices=CALL_STATUS, max_length=11, default='NOT_CALLED')
    needs_callback = models.CharField(choices=FOLLOW_UP_CALL_NEED, null=True, blank=True, max_length=11)
    customer_info = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.customer_fullName} - {self.customer_phoneNumber}'


class ContactForm(ModelForm):
    class Meta:
        model = CustomerContact
        fields = ['customer_fullName', 'customer_phoneNumber']
