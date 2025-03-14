from django.contrib import admin


from account.models import Account
from userauths.models import User
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class AccountAdminModel(ImportExportModelAdmin):
    list_editable = ['account_status', 'account_balance', 'kyc_submitted', 'kyc_confirmed'] 
    list_display = ['user', 'account_number' ,'account_status', 'account_balance', 'kyc_submitted', 'kyc_confirmed'] 
    list_filter = ['account_status']
    search_fields = ['user__username', 'user__email', 'account_number']



admin.site.register(Account, AccountAdminModel)
