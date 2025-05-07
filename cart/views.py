from django.shortcuts import render , redirect
from .models import *
from order.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.

@login_required(login_url='accounts:auth_view')
def add_cart(request, id):
    product = Product.objects.get(id=id)
    response = {'status': 'error', 'message': 'درخواست نامعتبر'}

    if request.method == "POST":
        if product.status != 'None':
            var_id = request.POST.get('select')
            variant = Variants.objects.get(id=var_id)
            data = Cart.objects.filter(user_id=request.user.id, variant_id=var_id)
            check = 'yes' if data else 'no'
        else:
            variant = None
            data = Cart.objects.filter(user_id=request.user.id, product_id=id)
            check = 'yes' if data else 'no'

        cart_form = CartForm(request.POST)
        if cart_form.is_valid():
            quantity = cart_form.cleaned_data['quantity']

            # Check availability before modifying or adding to cart
            if product.status != 'None':
                available_stock = variant.amount
            else:
                available_stock = product.amount

            # If item already in cart
            if check == 'yes':
                if product.status != 'None':
                    cart_item = Cart.objects.get(user_id=request.user.id, product_id=id, variant_id=var_id)
                else:
                    cart_item = Cart.objects.get(user_id=request.user.id, product_id=id)

                if cart_item.quantity + quantity <= available_stock:
                    cart_item.quantity += quantity
                    cart_item.save()
                    response = {'status': 'updated', 'message': 'تعداد به‌روزرسانی شد'}
                else:
                    response = {'status': 'error', 'message': 'موجودی کافی نیست'}
            else:
                if quantity <= available_stock:
                    if product.status != 'None':
                        Cart.objects.create(user_id=request.user.id, product_id=id, variant_id=var_id, quantity=quantity)
                    else:
                        Cart.objects.create(user_id=request.user.id, product_id=id, quantity=quantity)
                    response = {'status': 'added', 'message': 'محصول به سبد اضافه شد'}
                else:
                    response = {'status': 'error', 'message': 'موجودی کافی نیست'}

    return JsonResponse(response)


@login_required(login_url='accounts:auth_view')
def remove_cart(request , id ):
    url = request.META.get('HTTP_REFERER')
    Cart.objects.filter(id = id).delete()
    return redirect(url)
@login_required(login_url='accounts:auth_view')
def show_cart(request):
    cart = Cart.objects.filter(user_id=request.user.id)
    order_form = OrderForm()
    user = request.user
    total = 0
    for item in cart:
        if item.product.status != 'None':
            total += item.variant.total_price * item.quantity
        else :
            total += item.product.total_price * item.quantity
    return render(request , 'cart/cart.html' , {'cart':cart , 'order_form' : order_form , 'user' : user , 'total': total})

@login_required(login_url='accounts:auth_view')
def increase_cart(request, id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart.objects.get(id = id)
    if cart.product.status != 'None':
        variant = Variants.objects.get(id = cart.variant.id)
        if variant.amount > cart.quantity :
            cart.quantity += 1
            cart.save()
    else :
        product = Product.objects.get(id=cart.product.id)
        if product.amount > cart.quantity:
            cart.quantity += 1
            cart.save()

    return redirect(url)

@login_required(login_url='accounts:auth_view')
def decrease_cart(request , id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart.objects.get(id = id)
    if cart.quantity <= 1 :
        cart.delete()
    else :
        cart.quantity -= 1
        cart.save()
    return redirect(url)