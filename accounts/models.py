from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import jdatetime
from django_jalali.db import models as jmodels
from django.utils import timezone



class UserManager(BaseUserManager):
    def create_user(self, f_name, l_name, phone_number, codemeli, birthdate, gender, address, email, password=None):
        if not phone_number:
            raise ValueError('پر کردن فیلد شماره موبایل الزامی است')

        user = self.model(
            f_name=f_name,
            l_name=l_name,
            phone_number=phone_number,
            codemeli=codemeli,
            birthdate=birthdate,
            gender=gender,
            address=address,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password):
        user = self.create_user(
            f_name='admin',
            l_name='admin',
            phone_number=phone_number,
            codemeli='',
            birthdate=timezone.now(),
            gender='M',
            address='Admin Address',
            email='admin@example.com',
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    GENDER_CHOICES = (
        ('F', 'زن'),
        ('M', 'مرد'),
    )
    f_name = models.CharField(max_length=100 )
    l_name = models.CharField(max_length=100 )
    phone_number = models.CharField(unique=True, max_length=11)
    codemeli = models.CharField(max_length=11, blank=True, unique=True ,null=True)
    birthdate = jmodels.jDateField(null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=3, null=True, blank=True )
    address = models.TextField(null=True, blank=True)
    email = models.EmailField( blank=True, null=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['f_name', 'l_name']

    objects = UserManager()

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin