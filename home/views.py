from .forms import *
from django.shortcuts import render, redirect
from .models import *
# Create your views here.
from django.shortcuts import render
from .models import Product, Category
from django.core.paginator import Paginator
from cart.models import *
from django.contrib.auth.decorators import login_required
from .filters import ProductFilter
from django.http import JsonResponse


def show_products(request, id):
    products = Product.objects.all()
    category = Category.objects.all()
    form_search = SearchForm()
    data = Category.objects.get(id=id)
    products = products.filter(category=data)
    paginator = Paginator(products, 3)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return render(request, 'home/products.html', {'products': page_obj, 'data': data, 'form_search': form_search})

def product_search_inner(request, category_id):
    query = request.GET.get('inner-search', '')
    data = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=data)
    products = products.filter(product_name__icontains=query)

    product_filter = ProductFilter(request.GET, queryset=products)
    filtered_products = product_filter.qs

    product_data_inner = []
    for product in filtered_products:
        product_data_inner.append({
            'name': product.product_name,
            'price': product.fee,
            'image': product.product_img.url,
            'discount': product.discount,
            'weight': product.weight,
            'fee': product.fee,
            'id': product.id,
            'info': product.info,
            'average': product.average,
        })

    return JsonResponse({'products': product_data_inner})


def home(request):
    category = Category.objects.filter(sub_category_accessory=False, is_brand=False)
    slider = SliderHomeGallery.objects.all()
    popular_products = Product.objects.order_by('-like')[:20]
    video_section = AdvertisingVideo.objects.order_by('-id').first()
    form_contact = ContactForm()
    return render(request, 'home/home.html',
                  {'category': category, 'slider': slider, 'popular_products': popular_products,
                   'video_section': video_section, 'form_contact': form_contact})


def all_categories(request, slug, id):
    selected_cat = Category.objects.get(id=id, slug=slug)  # دریافت دسته انتخاب شده
    # فقط زیرمجموعه‌های غیر برند
    subcategories = selected_cat.subcategories.all()
    # فقط زیرمجموعه‌های برند
    subBrands = selected_cat.brand_subcategories.all()

    if subBrands.exists():
        category = subBrands
    elif subcategories.exists():
        category = subcategories
    else:
        return redirect('home:show_products', selected_cat.id)

    return render(request, 'home/inner_category.html', {'category': category})


def product_details(request, id):
    product = Product.objects.get(id=id)
    similar = product.tags.similar_objects()[:5]
    gallery = ProductGallery.objects.filter(product_gallery=product)
    cart_form = CartForm()
    comment_form = CommentForm()
    reply_form = replyForm()
    product_comments = Comments.objects.filter(product_id=id, is_reply=False)
    is_saved = product.saved_by_users.filter(id=request.user.id).exists()
    is_liked = product.like.filter(id=request.user.id).exists()
    variant = Variants.objects.filter(product_variant_id=id)
    for comment in product_comments:
        comment.is_liked_by_user = comment.comment_like.filter(id=request.user.id).exists()
    paginator = Paginator(product_comments, 3)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    # بررسی اینکه وضعیت محصول None نباشه
    if product.status != 'None':
        try:
            if request.method == 'POST':
                var_id = request.POST.get('select')
                variants = Variants.objects.get(id=var_id)
            else:
                variants = variant.first()
        except Variants.DoesNotExist:
            # اگر ID اشتباه بود، می‌تونیم یه مقدار پیش‌فرض بدیم
            variants = variant.first()

        return render(request, 'home/details.html', {
            'product': product,
            'variants': variants,  # گزینه انتخاب‌شده
            'variant': variant,  # لیست همه
            'gallery': gallery,
            'is_saved': is_saved,
            'is_liked': is_liked,
            'cart_form': cart_form,
            'similar': similar,
            'comment_form': comment_form,
            'product_comments': page_obj,
            'reply_form': reply_form,

        })
    else:
        return render(request, 'home/details.html', {
            'product': product,
            'gallery': gallery,
            'is_saved': is_saved,
            'is_liked': is_liked,
            'cart_form': cart_form,
            'similar': similar,
            'comment_form': comment_form,
            'product_comments': page_obj,
            'reply_form': reply_form,
        })


@login_required(login_url='accounts:auth_view')
def product_save(request, id):
    product = Product.objects.get(id=id)
    saved = False

    if product.saved_by_users.filter(id=request.user.id).exists():
        product.saved_by_users.remove(request.user)
    else:
        product.saved_by_users.add(request.user)
        saved = True
    save_count = product.saved_by_users.count()
    data = {
        'status': 'saved' if saved else 'unsaved',
        'filled_icon': 'bi-bookmark-fill',
        'unfilled_icon': 'bi-bookmark',
        'active_text': 'ذخیره ',
        'inactive_text': 'حذف ذخیره',
        'message': 'ذخیره شد',
        'save_count': save_count
    }
    return JsonResponse(data)


def all_products(request):
    category = Category.objects.all()
    products = Product.objects.all()

    product_filter = ProductFilter(request.GET, queryset=products)
    filtered_products = product_filter.qs

    paginator = Paginator(filtered_products, 8)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    return render(request, 'home/all-products.html', {
        'products': page_obj,
        'category': category,
        'filter': product_filter
    })


def product_search_all(request):
    query = request.GET.get('all-search', '')
    products = Product.objects.filter(product_name__icontains=query)
    product_filter = ProductFilter(request.GET, queryset=products)
    filtered_products = product_filter.qs

    all_product_data = []
    for product in filtered_products:
        all_product_data.append({
            'name': product.product_name,
            'price': product.fee,
            'image': product.product_img.url,
            'discount': product.discount,
            'weight': product.weight,
            'fee': product.fee,
            'id': product.id,
            'info': product.info,
            'average': product.average,
        })

    return JsonResponse({'products': all_product_data})


@login_required(login_url='accounts:auth_view')
def show_saved_products(request):
    products = request.user.save_product_user.all()
    category = Category.objects.all()
    product_filter = ProductFilter(request.GET, queryset=products)
    filtered_products = product_filter.qs
    paginator = Paginator(filtered_products, 8)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return render(request, 'home/save.html', {'products': page_obj, 'category': category,
                                              'filter': product_filter})


def product_search_save(request):
    query = request.GET.get('save-search', '')
    products = request.user.save_product_user.all()
    products = products.filter(product_name__icontains=query)
    product_filter = ProductFilter(request.GET, queryset=products)
    filtered_products = product_filter.qs

    product_data = []
    for product in filtered_products:
        product_data.append({
            'name': product.product_name,
            'price': product.fee,
            'image': product.product_img.url,
            'discount': product.discount,
            'weight': product.weight,
            'fee': product.fee,
            'id': product.id,
            'info': product.info,
            'average': product.average,
        })

    return JsonResponse({'products': product_data})


@login_required(login_url='accounts:auth_view')
def like_product(request, id):
    product = Product.objects.get(id=id)
    liked_product = False
    if product.like.filter(id=request.user.id).exists():
        product.like.remove(request.user)
    else:
        product.like.add(request.user)
        liked_product = True
    like_product_count = product.like.count()

    data = {
        'status': 'liked_product' if liked_product else 'unliked_product',
        'filled_icon': 'bi-suit-heart-fill',
        'unfilled_icon': 'bi-suit-heart',
        'active_text': 'لایک ',
        'inactive_text': 'حذف لایک',
        'message': ' محصول لایک شد',
        'like_product_count': like_product_count
    }
    return JsonResponse(data)


@login_required(login_url='accounts:auth_view')
def like_comment(request, id):
    selected_comment = Comments.objects.get(id=id)
    comment_liked = False
    if selected_comment.comment_like.filter(id=request.user.id).exists():
        selected_comment.comment_like.remove(request.user)
    else:
        selected_comment.comment_like.add(request.user)
        comment_liked = True
    comment_liked_count = selected_comment.comment_like.count()
    data = {
        'status': 'comment_liked' if comment_liked else 'comment_unliked',
        'filled_icon': 'bi-suit-heart-fill',
        'unfilled_icon': 'bi-suit-heart',
        'active_text': 'لایک ',
        'inactive_text': 'حذف لایک',
        'message': ' کامنت لایک شد',
        'comment_liked_count': comment_liked_count
    }
    return JsonResponse(data)


def contact_customer(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form_contact = ContactForm(request.POST)
        if form_contact.is_valid():
            form_contact.save()
    return redirect(url)


@login_required(login_url='accounts:auth_view')
def product_comment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            data = comment_form.cleaned_data
            Comments.objects.create(
                comment=data['comment'],
                rate=data['rate'],
                user_id=request.user.id,
                product_id=id,
            )
    return redirect(url)


@login_required(login_url='accounts:auth_view')
def comment_reply(request, id_product, id_comment):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        reply_form = replyForm(request.POST)
        if reply_form.is_valid():
            data = reply_form.cleaned_data
            Comments.objects.create(
                comment=data['reply'],
                user_id=request.user.id,
                product_id=id_product,
                reply_id=id_comment,
                is_reply=True

            )
    return redirect(url)
