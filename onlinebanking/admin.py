from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.contrib.auth.forms import UserCreationForm as UserCreationFormBase
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from onlinebanking.models import User
from onlinebanking.models import Account
from onlinebanking.models import Transaction
from onlinebanking.models import Trigger
from onlinebanking.models import UserTrigger
from onlinebanking.models import AccountTrigger
from onlinebanking.models import TransactionTrigger
from onlinebanking.models import Notification

class UserCreationForm(UserCreationFormBase):
    class Meta(UserCreationFormBase.Meta):
        model = User
        fields = UserCreationFormBase.Meta.fields + ('email', 'phone_number')

class UserAdmin(UserAdminBase):
    fieldsets = UserAdminBase.fieldsets
    for fieldset in fieldsets:
        if fieldset[0] == 'Personal info':
            fieldset[1]['fields'] += ('phone_number',)
    
    add_fieldsets = UserAdminBase.add_fieldsets
    for fieldset in UserAdminBase.add_fieldsets:
        fieldset[1]['fields'] = ('first_name', 'last_name') + fieldset[1]['fields']
        fieldset[1]['fields'] += ('email', 'phone_number',)

    search_fields = UserAdminBase.search_fields + ('phone_number',)

class AccountAdmin(admin.ModelAdmin):
    readonly_fields=('last_transaction_number',)

class TransactionAdmin(admin.ModelAdmin):
    readonly_fields=('posted',)

class TriggerAdmin(admin.ModelAdmin):
    readonly_fields=('trigger_count',)

class UserTriggerAdmin(admin.ModelAdmin):
    readonly_fields=('trigger_count',)

class AccountTriggerAdmin(admin.ModelAdmin):
    readonly_fields=('trigger_count',)

class TransactionTriggerAdmin(admin.ModelAdmin):
    readonly_fields=('trigger_count',)

class NotificationAdmin(admin.ModelAdmin):
    readonly_fields=('created',)

admin.site.unregister(Group)

admin.site.register(User, UserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Trigger, TriggerAdmin)
admin.site.register(UserTrigger, UserTriggerAdmin)
admin.site.register(AccountTrigger, AccountTriggerAdmin)
admin.site.register(TransactionTrigger, TransactionTriggerAdmin)
admin.site.register(Notification, NotificationAdmin)
