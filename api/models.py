from django.utils import timezone
from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User_record(AbstractBaseUser):
    user = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role_name = models.CharField(max_length=50)
    created_date = models.DateTimeField(default=timezone.now, blank=True, null=True, editable=False)
    reporting_to = models.CharField(max_length=50)
    #control --> REporting to

    sales_tracker = models.BooleanField(default=False)
    user_management = models.BooleanField(default=False)
    quality = models.BooleanField(default=False)
    procurement = models.BooleanField(default=False)
    quote_generator = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['']  # Add any additional required fields for user creation

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)

        # Check if the role_name is "Manager" and set corresponding boolean fields to True
        if self.role_name == "Manager" or self.role_name == "Teamlead" or self.role_name == "admin":
            self.sales_tracker = True
            self.user_management = True
            self.quality = True
            self.procurement = True
            self.quote_generator = True

        super().save(*args, **kwargs)

    def __str__(self):
        return self.user


class AckMail(models.Model):
    reference_number = models.CharField(max_length=255)
    sales_mail = models.CharField(max_length=255)
    sales_email_time = models.CharField(max_length=255)
    client_email = models.CharField(max_length=255)
    client_email_time = models.CharField(max_length=255)
    client_cc = models.TextField()
    client_subject = models.CharField(max_length=255)
    email_body =  models.FileField(upload_to='file')
    attachment =  models.FileField(upload_to='file')
    plain_text = models.TextField()
    sales_person_name = models.TextField()
    client_person_name = models.TextField()
    quotation_time = models.TextField()
    quotation_to = models.TextField()
    quotation_from = models.TextField()
    quotation_subject = models.TextField()
    quotation_plain_body = models.TextField()
    quotation_html_body =  models.FileField(upload_to='file')
    quotation_attachment =  models.FileField(upload_to='file')
    total_order_value = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)
    currency_value = models.CharField(max_length=255)
    reminder_status = models.CharField(max_length=255)
    ack_time = models.CharField(max_length=255)
    order_ageing = models.CharField(max_length=255)
    order_date_time = models.CharField(max_length=255)
    order_closure_days = models.CharField(max_length=255)
    order_value = models.CharField(max_length=255)
    order_email_attachment = models.CharField(max_length=255)


  
