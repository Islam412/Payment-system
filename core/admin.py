from django.contrib import admin

from core.models import Transaction , CreditCard , Notification , Home


# Register your models here.

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['amount' , 'status' , 'transaction_type' , 'reciever' , 'sender']
    list_display = ['user' , 'amount' , 'status' , 'transaction_type' , 'reciever' , 'sender']




class CreditCardAdmin(admin.ModelAdmin):
    list_display = ['amount' , 'card_type']
    list_display = ['user' , 'amount' , 'card_type']




class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'amount' ,'date']


admin.site.register(Transaction , TransactionAdmin)
admin.site.register(CreditCard , CreditCardAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Home)
