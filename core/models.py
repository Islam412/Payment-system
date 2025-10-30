from django.db import models
from django.utils.translation import gettext_lazy as _

from shortuuid.django_fields import ShortUUIDField

from userauths.models import User
from account.models import Account



# Create your models here.
TRANSACTION_TYPE = (
    ("Transfer", "Transfer"),
    ("Recieved", "Recieved"),
    ("Withdraw", "Withdraw"),
    ("Refund", "Refund"),
    ("request", "Payment Request"),
    ("none", "None")
)

TRANSACTION_STATUS = (
    ("failed", "Failed"),
    ("completed", "Completed"),
    ("pending", "Pending"),
    ("processing", "Processing"),
    ("request_sent", "Request Sent"),
    ("request_settled", "Request Settled"),
    ("request_processing", "Request Processing"),
)

CARD_TYPE = (
    ("Master", "Master"),
    ("Visa", "Visa"),
    ("Verve", "Verve"),

)

NOTIFICATION_TYPE = (
    ("None", "None"),
    ("Transfer", "Transfer"),
    ("Credit Alert", "Credit Alert"),
    ("Debit Alert", "Debit Alert"),
    ("Sent Payment Request", "Sent Payment Request"),
    ("Recieved Payment Request", "Recieved Payment Request"),
    ("Funded Credit Card", "Funded Credit Card"),
    ("Withdrew Credit Card Funds", "Withdrew Credit Card Funds"),
    ("Deleted Credit Card", "Deleted Credit Card"),
    ("Added Credit Card", "Added Credit Card"),

)



class Transaction(models.Model):
    transaction_id = ShortUUIDField(unique=True, length=15, max_length=20, prefix="TRN")
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    description = models.CharField(max_length=1000, null=True, blank=True)
    
    reciever = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reciever")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")
   
    reciever_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="reciever_account")
    sender_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="sender_account")
    
    status = models.CharField(choices=TRANSACTION_STATUS, max_length=100, default="pending")
    transaction_type = models.CharField(choices=TRANSACTION_TYPE, max_length=100, default="none")
    
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    
    def __str__(self):
        try:
            return f"{self.user}"
        except:
            return f"Transaction"
        


class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_id = ShortUUIDField(unique=True, length=5, max_length=20, prefix="CARD", alphabet="1234567890")

    name = models.CharField(max_length=100)
    number = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    cvv = models.IntegerField()

    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    card_type = models.CharField(choices=CARD_TYPE, max_length=20, default="Master")

    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notification_type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE, default="none")
    amount = models.IntegerField(default=0)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    nid = ShortUUIDField(length=10, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz")
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Notification"

    def __str__(self):
        return f"{self.user} - {self.notification_type}"
    


class Home(models.Model):
    image = models.ImageField(upload_to="image home")
    supported_currencies = models.PositiveIntegerField()
    available_countries = models.PositiveIntegerField()
    payment_methods = models.PositiveIntegerField()
    support_team_day = models.PositiveIntegerField(default=7)
    support_team_hour = models.PositiveIntegerField(default=24)
    peace_of_mind = models.CharField(max_length=1000)
    business_ready = models.CharField(max_length=1000)
    transparent = models.CharField(max_length=1000)
    international_network = models.CharField(max_length=1000)
    payments = models.CharField(max_length=1000)
    collections = models.CharField(max_length=1000)
    conversions = models.CharField(max_length=1000)
    global_account = models.CharField(max_length=1000)
    register_for_free = models.CharField(max_length=1000)
    set_up_your_transfer = models.CharField(max_length=1000)
    make_your_payment = models.CharField(max_length=1000)
    you_all_done = models.CharField(max_length=1000)







class Company(models.Model):
    name = models.CharField(_('name'),max_length=255)
    logo = models.ImageField(_('logo'),upload_to='company_logos')
    see_how_it_Works = models.FileField(_('See How it Works'),upload_to='videos')
    address = models.CharField(_('address'),max_length=255)
    support_mail = models.EmailField(_('Support Mail'),max_length=200, null=True, blank=True)
    phone_number = models.CharField(_('Phone Number'),max_length=255, null=True, blank=True)
    android_app = models.URLField(_('android app'),max_length=200, null=True, blank=True)
    ios_app = models.URLField(_('ios app'),max_length=200, null=True, blank=True)

    # FAQ
    how_to_send_money_online = models.CharField(max_length=1000)
    how_much_are_money_transfer_fees = models.CharField(max_length=1000)
    what_is_the_fastest_way_to_send_money_abroad = models.CharField(max_length=1000)
    how_to_use_app = models.CharField(max_length=1000)
    how_does_Paylio_protect_your_money = models.CharField(max_length=1000)
    are_money_transfer_apps_safe = models.CharField(max_length=1000)
    how_much_money_can_i_send = models.CharField(max_length=1000)
    which_currency_can_i_send = models.CharField(max_length=1000)
    Cancel_transaction = models.CharField(max_length=1000)
    Can_i_send_multiple_payments = models.CharField(max_length=1000)

    # about us
    secure_payments = models.CharField(_('Secure Payments'),max_length=255)
    fast_processing = models.CharField(_('Fast Processing'),max_length=255)
    global_coverage = models.CharField(_('Global Coverage'),max_length=255)
    our_mission = models.CharField(_('Our Mission'),max_length=255)
    our_vision = models.CharField(_('Our Vision'),max_length=255)
    transactions = models.CharField(_('Transactions'),max_length=255)
    system_uptime = models.CharField(_('System Uptime'),max_length=255)


    def __str__(self):
        return self.name



