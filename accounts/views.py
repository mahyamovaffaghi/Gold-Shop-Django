from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from order.models import *
from django.core.paginator import Paginator
from .filters import *
# Create your views here.


def auth_view(request):
    reg_form = UserRegisterForm()
    login_form = UserLoginForm()

    if request.method == 'POST':
        if 'register' in request.POST:
            reg_form = UserRegisterForm(request.POST)
            if reg_form.is_valid():
                reg_form.save()
                return redirect("home:home")

        elif 'login' in request.POST:
            login_form = UserLoginForm(request.POST)
            if login_form.is_valid():
                data = login_form.cleaned_data
                user = authenticate(request, username=data['user'], password=data['password'])

                if user is not None:
                    login(request, user)
                    return redirect("home:home")
                else:
                    print('نام کاربری یا رمز عبور اشتباه است')

    return render(request, 'accounts/auth.html', {'reg_form': reg_form, 'login_form': login_form})
@login_required(login_url='accounts:auth_view')
def logout_user(request):
    logout(request)
    return redirect('accounts:auth_view')

@login_required(login_url='accounts:auth_view')
def profile_view(request):
    if request.method == 'POST':
        print(request.POST)
        prof_form = UserUpdateProfileForm(request.POST, instance=request.user)
        if prof_form.is_valid():
            prof_form.save()
            print('Profile changed!')
            return redirect('accounts:profile_view')  # اینجا ریدایرکت میکنیم

    else:
        prof_form = UserUpdateProfileForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'prof_form': prof_form})



def forget_password (request):
    return render(request, 'accounts/forget.html' )

@login_required(login_url='accounts:auth_view')
def history_view(request):
    base_qs = ItemOrder.objects.filter(user_id=request.user.id).select_related('order', 'product', 'variant')

    order_filter = OrderPaidFilter(request.GET, queryset=base_qs)

    paginator = Paginator(order_filter.qs, 10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    return render(request, 'accounts/history.html', {
        'data': page_obj,
        'order_form': SearchOrderForm(),
        'order_filter': order_filter
    })
@login_required(login_url='accounts:auth_view')
def order_search(request):
    data = ItemOrder.objects.all()
    if request.method == 'POST':
        order_form = SearchOrderForm(request.POST)
        if order_form.is_valid():
            data_order = order_form.cleaned_data['search_order']
            if data_order is not None:
                data = data.filter(product__product_name__icontains=data_order)
            return  render(request , 'accounts/history.html' , {'data':data  , 'order_form':order_form} )
