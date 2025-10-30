from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _


import uuid
from shortuuid.django_fields import ShortUUIDField

from userauths.models import User

# Create your models here.


def user_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s_%s" % (instance.id, ext)
    return "user_{0}/{1}".format(instance.user.id, filename)



ACCOUNT_STATUS = (
    ("active", "Active"),
    ("pending", "Pending"),
    ("in-active", "In-active")
)

class Account(models.Model):
    id = models.UUIDField(_('id'),primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user =  models.OneToOneField(User, on_delete=models.CASCADE,verbose_name=_('user'))
    account_balance = models.DecimalField(_('account balance'),max_digits=12, decimal_places=2, default=0.00)
    account_number = ShortUUIDField(_('account number'),unique=True,length=10, max_length=25, prefix="217", alphabet="1234567890")
    account_id = ShortUUIDField(_('account id'),unique=True,length=7, max_length=25, prefix="DEX", alphabet="1234567890")
    pin_number = ShortUUIDField(_('pin number'),unique=True,length=4, max_length=7, alphabet="1234567890") #2737
    red_code = ShortUUIDField(_('red code'),unique=True,length=10, max_length=20, alphabet="abcdefgh1234567890")
    account_status = models.CharField(_('account status'),max_length=100, choices=ACCOUNT_STATUS, default="in-active")
    date = models.DateTimeField(_('date'),auto_now_add=True)
    kyc_submitted = models.BooleanField(_('kyc submitted'),default=False)
    kyc_confirmed = models.BooleanField(_('kyc confirmed'),default=False)
    recommended_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="recommended_by",verbose_name=_('recommended by'))
    review = models.CharField(_('review'),max_length=100, null=True, blank=True, default="Review")

    
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user}"


def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

def save_account(sender, instance,**kwargs):
    instance.account.save()

post_save.connect(create_account, sender=User)
post_save.connect(save_account, sender=User)


MARITAL_STATUS = (
    ("married", "Married"),
    ("single", "Single"),
    ("other", "Other")
)

GENDER = (
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other")
)


IDENTITY_TYPE = (
    ("national_id_card", "National ID Card"),
    ("drivers_licence", "Drives Licence"),
    ("international_passport", "International Passport")
)

class KYC(models.Model):
    id = models.UUIDField(_('id'),primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user =  models.OneToOneField(User, on_delete=models.CASCADE,verbose_name=_('user'))
    account =  models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True,verbose_name=_('account'))
    full_name = models.CharField(_('full name'),max_length=1000)
    image = models.ImageField(_('image'),upload_to="kyc", default="default.jpg")
    marrital_status = models.CharField(_('marrital status'),choices=MARITAL_STATUS, max_length=40)
    gender = models.CharField(_('gender'),choices=GENDER, max_length=40)
    identity_type = models.CharField(_('identity type'),choices=IDENTITY_TYPE, max_length=140)
    identity_image = models.ImageField(_('identity image'),upload_to="kyc", null=True, blank=True)
    date_of_birth = models.DateTimeField(_('date of birth'),auto_now_add=False)
    signature = models.ImageField(_('signature'),upload_to="kyc")

    # Address
    country = models.CharField(_('country'),max_length=100)
    state = models.CharField(_('state'),max_length=100)
    city = models.CharField(_('city'),max_length=100)

    # Contact Detail
    mobile = models.CharField(_('mobile'),max_length=1000)
    fax = models.CharField(_('fax'),max_length=1000)
    date = models.DateTimeField(_('date'),auto_now_add=True)


    def __str__(self):
        return f"{self.user}"    

    
    class Meta:
        ordering = ['-date']
