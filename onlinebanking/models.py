from decimal import Decimal

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


DECIMAL_MAX = 15
class User(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=150, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)
    email = models.EmailField(_('email address'), blank=False, unique=True)
    phone_regex = RegexValidator(regex=r'^\D?([2-9]\d{2})\D?\D?(\d{3})\D?(\d{4})$$', message="Phone number must be entered in the format: '800-555-5555'")
    phone_number = models.CharField(validators=[phone_regex], max_length=14, blank=True)

    def clean(self):
        
        if self.phone_number:
            tmp_phonenum = self.phone_number
            tmp_phonenum = ''.join(i for i in tmp_phonenum if i.isdigit())
            self.phone_number = f"{tmp_phonenum[0:3]}-{tmp_phonenum[3:6]}-{tmp_phonenum[6:10]}"

    def save(self, *args, **kwargs): 
        super(User, self).save(*args, **kwargs)

        user_trigger, created = UserTrigger.objects.get_or_create(user=self)
        if created:
            user_trigger.name = "Account Changes Alert"
            user_trigger.save()
            
        if self.phone_number:
            if created:
                user_trigger.sms = True
                user_trigger.save()
        else:
            user_trigger.sms = False
            user_trigger.save()
           

    def __str__(self):
        return self.username

class Account(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    account_number = models.BigIntegerField(unique=True)
    last_transaction_number = models.IntegerField(default=10000, editable=False)
    mock_transactions = models.BooleanField(default=False)
    
    class AccountType(models.TextChoices):
        CHECKING = 'CHECKING', _('Checking')
        SAVINGS = 'SAVINGS', _('Savings')

    account_type = models.CharField(
        max_length=8,
        choices=AccountType.choices,
        default=AccountType.CHECKING,
    )
    balance = models.DecimalField(max_digits=DECIMAL_MAX, decimal_places=2, default=Decimal('0.00'))

    def clean(self):
        if len(str(self.account_number)) != 8:
            raise ValidationError(
                {'account_number': ['Account number is not 8 digits.',]},
            )

    class Meta:
        ordering = ['account_type',]

    def __str__(self):
        return f'{self.account_type} | ****{str(self.account_number)[-4:]}'

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_number = models.IntegerField()
    posted = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=DECIMAL_MAX, decimal_places=2)
    description = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=DECIMAL_MAX, decimal_places=2, default=Decimal('0.00'), editable=False)

    @property
    def type(self):
        if self.amount < 0:
            return 'DEBIT'
        else:
            return 'CREDIT'

    class Meta:
        ordering = ['-posted',]

    def __str__(self):
        return f'{self.account} {self.transaction_number} | {self.amount} - {self.description}'

class Trigger(models.Model):
    name = models.CharField(max_length=60, blank=True)
    sms = models.BooleanField(default=False)
    email = models.BooleanField(default=True)
    enabled = models.BooleanField(default=True)
    trigger_count = models.PositiveIntegerField(default=0, editable=False)

    def clean(self):
        if not hasattr(self, 'user'):
            return

        if self.sms and not self.user.phone_number:
            raise ValidationError(
                {'sms': ['No phone number associated with account.',]},
            )

        if self.email and not self.user.email:
            raise ValidationError(
                {'email': ['No email associated with account.']},
            )


    def __str__(self):
        return f'{self.id}'

class UserTrigger(Trigger):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    on_login = models.BooleanField(default=True)
    on_change = models.BooleanField(default=True)

class AccountTrigger(Trigger):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)

    balance_gte = models.DecimalField(max_digits=DECIMAL_MAX, decimal_places=2, blank=True, null=True)
    balance_lte = models.DecimalField(max_digits=DECIMAL_MAX, decimal_places=2, blank=True, null=True)

    def clean(self):
        if not self.balance_gte and not self.balance_lte:
            raise ValidationError(
                {'balance_gte': ['Cannot be empty if Less than is empty.'],
                 'balance_lte': ['Cannot be empty if Greater than is empty.']},
            )

class TransactionTrigger(Trigger):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)

    type_credit = models.BooleanField(default=False)
    type_debit = models.BooleanField(default=False)

    start = models.TimeField(blank=True, null=True)
    end = models.TimeField(blank=True, null=True)
    
    amount_gte = models.DecimalField(max_digits=DECIMAL_MAX, decimal_places=2, blank=True, null=True)
    amount_lte = models.DecimalField(max_digits=DECIMAL_MAX, decimal_places=2, blank=True, null=True)

    description_value = models.CharField(max_length=100, blank=True)

    def clean(self):
        if not self.type_credit and not self.type_debit:
            raise ValidationError(
                {'type_credit': ['Check type_debit or type_credit'],
                 'type_debit': ['Check type_debit or type_credit']},
            )

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    triggered_by = models.ForeignKey(Trigger, null=True, on_delete=models.CASCADE)
    email_sent = models.DateTimeField(blank=True, null=True)
    sms_sent = models.DateTimeField(blank=True, null=True)
    read = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField(default=False)
    title = models.CharField(max_length=50)
    message = models.TextField()

    class Meta:
        ordering = ['-created',]
