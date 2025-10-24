from django.db import models

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
    video = models.FileField(upload_to='videos')
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
    android_app = models.URLField(max_length=500, blank=True, null=True)
    ios_app = models.URLField(max_length=500, blank=True, null=True)


