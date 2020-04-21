from django import forms
from django.contrib.auth import forms as auth_forms
from .models import *

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ('user', 'balance')

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ('transaction_number', 'account')

class TriggerForm(forms.ModelForm):
    class Meta:
        model = Trigger
        exclude = ('user', 'trigger_count',)

    def __init__(self, user, *args, **kwargs):
        super(TriggerForm, self).__init__(*args, **kwargs)
        if not user.phone_number:
            self.initial['sms'] = False
            self.fields['sms'].disabled = True
            self.fields['sms'].help_text = "No phone number associated with account."

        if not user.email:
            self.initial['email'] = False
            self.fields['email'].disabled = True
            self.fields['email'].help_text = "No email associated with account."

class UserTriggerForm(TriggerForm):
    class Meta(TriggerForm.Meta):
        model = UserTrigger

    def __init__(self, user, *args, **kwargs):
        super(UserTriggerForm, self).__init__(user, *args, **kwargs)

class AccountTriggerForm(TriggerForm):
    class Meta(TriggerForm.Meta):
        model = AccountTrigger
        
    def __init__(self, user, *args, **kwargs):
        super(AccountTriggerForm, self).__init__(user, *args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(user=user)

class TransactionTriggerForm(TriggerForm):
    class Meta(TriggerForm.Meta):
        model = TransactionTrigger

    def __init__(self, user, *args, **kwargs):
        super(TransactionTriggerForm, self).__init__(user, *args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(user=user)

class UserChangeForm(auth_forms.UserChangeForm):
    password = None
    class Meta(auth_forms.UserChangeForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')
