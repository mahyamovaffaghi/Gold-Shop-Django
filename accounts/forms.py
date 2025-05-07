from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django_jalali.admin.widgets import AdminjDateWidget
from django_jalali.forms import jDateField
class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="رمز عبور")
    password2 = forms.CharField(widget=forms.PasswordInput, label="تایید رمز عبور")
    birthdate = jDateField(widget=AdminjDateWidget(format='%Y/%m/%d'), required=False)
    class Meta:
        model = User
        fields = ['f_name', 'l_name', 'phone_number', 'codemeli', 'birthdate', 'gender', 'address', 'email']


    def clean_password2(self):
        data = self.cleaned_data
        if data['password1'] and data['password2'] and data['password1'] != data['password2']:
            raise forms.ValidationError('رمزهای عبور مطابقت ندارند')
        return data['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    birthdate = jDateField(widget=AdminjDateWidget(format='%Y/%m/%d'), required=False)

    class Meta:
        model = User
        fields = ['f_name', 'l_name', 'phone_number', 'codemeli', 'birthdate', 'gender', 'address', 'email']

    def clean_password(self):
        return self.initial['password']


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="رمز عبور")
    password2 = forms.CharField(widget=forms.PasswordInput, label="تایید رمز عبور")

    class Meta:
        model = User
        fields = ['f_name', 'l_name', 'phone_number']

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if User.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError('این شماره موبایل قبلاً ثبت شده است.')
        return phone

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('رمزهای عبور مطابقت ندارند.')
        if len(password2) < 8:
            raise forms.ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد.')
        if not any(x.isupper() for x in password2):
            raise forms.ValidationError('رمز عبور باید حداقل یک حرف بزرگ داشته باشد.')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    user = forms.CharField(label="شماره موبایل", max_length=12)
    password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور")


class UserUpdateProfileForm(forms.ModelForm):
    birthdate = jDateField(widget=AdminjDateWidget(format='%Y/%m/%d'), required=False)
    class Meta:
        model = User
        fields = ['f_name', 'l_name', 'phone_number', 'codemeli', 'birthdate', 'gender', 'address', 'email']

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if User.objects.filter(phone_number=phone_number).exclude(id = self.instance.id).exists():
            raise forms.ValidationError('این شماره موبایل قبلاً ثبت شده است.')
        return phone_number





class SearchOrderForm(forms.Form):
    search_order = forms.CharField(max_length=50)