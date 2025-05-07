from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from cart.models import Cart
from .forms import *
import jdatetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST



@login_required(login_url='accounts:auth_view')
def order_show(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    form_coupon = CouponForm()
    return render(request, 'order/order.html', {'order': order, 'form_coupon': form_coupon})

@login_required(login_url='accounts:auth_view')
def create_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            data = order_form.cleaned_data
            order = Order.objects.create(
                order_user_id=request.user.id,
                order_phoneNumber=data['order_phoneNumber'],
                order_firstName=data['order_firstName'],
                order_lastName=data['order_lastName'],
                order_address=data['order_address']
            )
            cart = Cart.objects.filter(user_id=request.user.id)
            for c in cart:
                ItemOrder.objects.create(
                    order_id=order.id,
                    user_id=request.user.id,
                    product_id=c.product_id,
                    variant_id=getattr(c, 'variant_id', None),
                    quantity=c.quantity
                )
            cart.delete()
            return redirect('order:order_show', order.id)

@login_required(login_url='accounts:auth_view')
def coupon_order(request, order_id):
    if request.method == 'POST':
        form_coupon = CouponForm(request.POST)
        time = jdatetime.datetime.now()
        if form_coupon.is_valid():
            code = form_coupon.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, start__lt=time, end__gte=time, coupon_active=True)
            except Coupon.DoesNotExist:
                print('we dont have this coupon code')
                return redirect('order:order_show', order_id)

            order = Order.objects.get(id=order_id)
            order.order_discount = coupon.discount
            order.save()
        return redirect('order:order_show', order_id)

@login_required(login_url='accounts:auth_view')
def paid(request, order_id):
    url = request.META.get('HTTP_REFERER')
    order = Order.objects.get(id=order_id)
    order.order_paid = True
    print('paid successfully!')
    order.save()
    item = ItemOrder.objects.filter(order_id=order_id)
    for c in item:
        if c.product.status == 'None':
            product = Product.objects.get(id=c.product.id)
            product.amount -= c.quantity
            product.sell += c.quantity
            product.save()
        else:
            variant = Variants.objects.get(id=c.variant.id)
            variant.amount -= c.quantity
            variant.save()
    return redirect(url)
