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
    transaction_id = ShortUUIDField(_('transaction id'),unique=True, length=15, max_length=20, prefix="TRN")
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,verbose_name=_('user'))
    amount = models.DecimalField(_('amount'),max_digits=12, decimal_places=2, default=0.00)
    description = models.CharField(_('description'),max_length=1000, null=True, blank=True)
    
    reciever = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reciever",verbose_name=_('reciever'))
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender",verbose_name=_('sender'))
   
    reciever_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="reciever_account",verbose_name=_('reciever account'))
    sender_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="sender_account",verbose_name=_('sender account'))
    
    status = models.CharField(_('status'),choices=TRANSACTION_STATUS, max_length=100, default="pending")
    transaction_type = models.CharField(_('transaction type'),choices=TRANSACTION_TYPE, max_length=100, default="none")
    
    date = models.DateTimeField(_('date'),auto_now_add=True)
    updated = models.DateTimeField(_('updated'),auto_now_add=False, null=True, blank=True)
    
    def __str__(self):
        try:
            return f"{self.user}"
        except:
            return f"Transaction"
        


class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name=_('user'))
    card_id = ShortUUIDField(_('card id'),unique=True, length=5, max_length=20, prefix="CARD", alphabet="1234567890")

    name = models.CharField(_('name'),max_length=100)
    number = models.IntegerField(_('number'))
    month = models.IntegerField(_('month'))
    year = models.IntegerField(_('year'))
    cvv = models.IntegerField(_('cvv'))

    amount = models.DecimalField(_('amount'),max_digits=12, decimal_places=2, default=0.00)

    card_type = models.CharField(_('card type'),choices=CARD_TYPE, max_length=20, default="Master")

    date = models.DateField(_('date'),auto_now_add=True)

    def __str__(self):
        return f"{self.user}"



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,verbose_name=_('user'))
    notification_type = models.CharField(_('notification type'),max_length=100, choices=NOTIFICATION_TYPE, default="none")
    amount = models.IntegerField(_('amount'),default=0)
    is_read = models.BooleanField(_('is read'),default=False)
    date = models.DateTimeField(_('date'),auto_now_add=True)
    nid = ShortUUIDField(_('nid'),length=10, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz")
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Notification"

    def __str__(self):
        return f"{self.user} - {self.notification_type}"
    


class Home(models.Model):
    image = models.ImageField(_('image'),upload_to="image home")
    supported_currencies = models.PositiveIntegerField(_('supported currencies'))
    available_countries = models.PositiveIntegerField(_('available countries'))
    payment_methods = models.PositiveIntegerField(_('payment methods'))
    support_team_day = models.PositiveIntegerField(_('support team day'),default=7)
    support_team_hour = models.PositiveIntegerField(_('support team hour'),default=24)
    peace_of_mind = models.CharField(_('peace of mind'),max_length=1000)
    business_ready = models.CharField(_('business ready'),max_length=1000)
    transparent = models.CharField(_('transparent'),max_length=1000)
    international_network = models.CharField(_('international network'),max_length=1000)
    payments = models.CharField(_('payments'),max_length=1000)
    collections = models.CharField(_('collections'),max_length=1000)
    conversions = models.CharField(_('conversions'),max_length=1000)
    global_account = models.CharField(_('global account'),max_length=1000)
    register_for_free = models.CharField(_('register for free'),max_length=1000)
    set_up_your_transfer = models.CharField(_('set up your transfer'),max_length=1000)
    make_your_payment = models.CharField(_('make your payment'),max_length=1000)
    you_all_done = models.CharField(_('you all done'),max_length=1000)







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
    how_to_send_money_online = models.CharField(_('how to send money online'),max_length=1000)
    how_much_are_money_transfer_fees = models.CharField(_('how much are money transfer fees'),max_length=1000)
    what_is_the_fastest_way_to_send_money_abroad = models.CharField(_('what is the fastest way to send money abroad'),max_length=1000)
    how_to_use_app = models.CharField(_('how_to_use_app'),max_length=1000)
    how_does_Paylio_protect_your_money = models.CharField(_('how does Paylio protect your money'),max_length=1000)
    are_money_transfer_apps_safe = models.CharField(_('are money transfer apps safe'),max_length=1000)
    how_much_money_can_i_send = models.CharField(_('how much money can i send'),max_length=1000)
    which_currency_can_i_send = models.CharField(_('which currency can i send'),max_length=1000)
    Cancel_transaction = models.CharField(_('Cancel transaction'),max_length=1000)
    Can_i_send_multiple_payments = models.CharField(_('Can i send multiple payments'),max_length=1000)

    # about us
    secure_payments = models.CharField(_('Secure Payments'),max_length=255)
    fast_processing = models.CharField(_('Fast Processing'),max_length=255)
    global_coverage = models.CharField(_('Global Coverage'),max_length=255)
    our_mission = models.CharField(_('Our Mission'),max_length=255)
    our_vision = models.CharField(_('Our Vision'),max_length=255)
    transactions = models.CharField(_('Transactions'),max_length=255)
    active_users = models.CharField(_('Active Users'),max_length=255)
    countries_supported = models.CharField(_('Countries Supported'),max_length=255)
    system_uptime = models.CharField(_('System Uptime'),max_length=255)


    def __str__(self):
        return self.name



