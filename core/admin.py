from django.contrib import admin

from core.models import Transaction


# Register your models here.

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['amount' , 'status' , 'transaction_type' , 'reciever' , 'sender']
    list_display = ['user' , 'amount' , 'status' , 'transaction_type' , 'reciever' , 'sender']




admin.site.register(Transaction , TransactionAdmin)
