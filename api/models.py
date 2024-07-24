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
    REQUIRED_FIELDS = ['']  

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        if self.role_name == "Manager" or self.role_name == "Teamlead" or self.role_name == "admin":
            self.sales_tracker = True
            self.user_management = True
            self.quality = True
            self.procurement = True
            self.quote_generator = True
        else:
            self.sales_tracker = True
            self.user_management = False
            self.quality = False
            self.procurement = False
            self.quote_generator = False

        super().save(*args, **kwargs)

    def __str__(self):
        return self.user

class ack_mail(models.Model):
    reference_number = models.CharField(max_length=255)
    sales_mail = models.CharField(max_length=255)
    sales_email_time = models.CharField(max_length=255)
    client_email = models.CharField(max_length=255)
    client_email_time = models.CharField(max_length=255)
    client_cc = models.TextField()
    client_subject = models.CharField(max_length=255)
    email_body = models.BinaryField()
    attachment = models.BinaryField()
    plain_text = models.TextField()
    sales_person_name = models.TextField()
    client_person_name = models.TextField()
    quotation_time = models.TextField()
    quotation_to = models.TextField()
    quotation_from = models.TextField()
    quotation_subject = models.TextField()
    quotation_plain_body = models.TextField()
    quotation_html_body = models.BinaryField()
    quotation_attachment = models.BinaryField()
    total_order_value = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)
    currency_value = models.CharField(max_length=255)
    reminder_status = models.CharField(max_length=255)
    ack_time = models.CharField(max_length=255)
    order_ageing = models.CharField(max_length=255)
    order_value = models.CharField(max_length=255)
    order_date_time = models.CharField(max_length=255)
    
    class Meta:
        managed = False
        db_table = 'ack_mail'




class CustomerFeedback(models.Model):
    
    form_timestamp = models.CharField(max_length=255)
    form_date = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)
    client_disignation = models.CharField(max_length=255)
    telephone_number = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    quality_rate = models.CharField(max_length=255)
    services_experience_rate = models.CharField(max_length=255)
    technical_enquires_rate = models.CharField(max_length=255)
    team_communication_rate = models.CharField(max_length=255)
    team_help_rate = models.CharField(max_length=255)
    product_quality_punctuality_rate = models.CharField(max_length=255)
    customer_statisfaction_rate = models.CharField(max_length=255)
    service_provider_rate = models.CharField(max_length=255)
    about_team_product_service = models.CharField(max_length=255)
    other_feedback = models.CharField(max_length=255)
    doc_file = models.BinaryField(null=True, blank=True)
    email_screenshot = models.BinaryField(null=False, blank=False)
    
    class Meta:
        db_table = 'customer_feedback'

    def __str__(self):
        return self.client_name





class PriceListV2(models.Model):
    item = models.CharField(max_length=255)
    winding_material = models.CharField(max_length=255)
    filler_material = models.CharField(max_length=255)
    inner_ring_material = models.CharField(max_length=255)
    outer_ring_material = models.CharField(max_length=255)
    material_size = models.CharField(max_length=255)
    rating = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    

    class Meta:
        db_table = 'price_list_v2'



from django.db import models

class MtcV3(models.Model):
    # Initially, we won't define any fields here
    pass

    class Meta:
        db_table = 'mtc_v3'