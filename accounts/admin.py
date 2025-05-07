from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django_jalali.admin.widgets import AdminjDateWidget
from .forms import UserChangeForm, UserCreateForm
from .models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreateForm
    list_display = ['f_name', 'l_name', 'phone_number', 'gender', 'birthdate', 'address', 'is_active']
    list_filter = ['is_active', 'gender']
    fieldsets = (
        ('User Info', {'fields': ('f_name', 'l_name', 'phone_number', 'email', 'password')}),
        ('Personal Info', {'fields': ('birthdate', 'gender', 'address')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    add_fieldsets = (
        (None, {'fields': ('f_name', 'l_name', 'phone_number', 'codemeli', 'birthdate', 'gender', 'address', 'email', 'password1', 'password2')}),
    )
    search_fields = ['phone_number', 'f_name', 'l_name']
    ordering = ['phone_number']
    filter_horizontal = []


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)