# Generated by Django 3.0.5 on 2020-05-02 02:14

from decimal import Decimal
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('phone_number', models.CharField(blank=True, max_length=14, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '800-555-5555'", regex='^\\D?([2-9]\\d{2})\\D?\\D?(\\d{3})\\D?(\\d{4})$$')])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.BigIntegerField(unique=True)),
                ('last_transaction_number', models.IntegerField(default=10000, editable=False)),
                ('mock_transactions', models.BooleanField(default=False)),
                ('account_type', models.CharField(choices=[('CHECKING', 'Checking'), ('SAVINGS', 'Savings')], default='CHECKING', max_length=8)),
                ('balance', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=15)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['account_type'],
            },
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=15)),
                ('sms', models.BooleanField(default=False)),
                ('email', models.BooleanField(default=True)),
                ('enabled', models.BooleanField(default=True)),
                ('trigger_count', models.PositiveIntegerField(default=0, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_number', models.IntegerField()),
                ('posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('description', models.CharField(max_length=100)),
                ('balance', models.DecimalField(decimal_places=2, default=Decimal('0.00'), editable=False, max_digits=15)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlinebanking.Account')),
            ],
            options={
                'ordering': ['-posted'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('email_sent', models.DateTimeField(blank=True, null=True)),
                ('sms_sent', models.DateTimeField(blank=True, null=True)),
                ('read', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=50)),
                ('message', models.TextField()),
                ('triggered_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='onlinebanking.Trigger')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='UserTrigger',
            fields=[
                ('trigger_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='onlinebanking.Trigger')),
                ('on_login', models.BooleanField(default=True)),
                ('on_change', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('onlinebanking.trigger',),
        ),
        migrations.CreateModel(
            name='TransactionTrigger',
            fields=[
                ('trigger_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='onlinebanking.Trigger')),
                ('type_credit', models.BooleanField(default=False)),
                ('type_debit', models.BooleanField(default=False)),
                ('start', models.TimeField(blank=True, null=True)),
                ('end', models.TimeField(blank=True, null=True)),
                ('amount_gte', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('amount_lte', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('description_value', models.CharField(blank=True, max_length=100)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='onlinebanking.Account')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('onlinebanking.trigger',),
        ),
        migrations.CreateModel(
            name='AccountTrigger',
            fields=[
                ('trigger_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='onlinebanking.Trigger')),
                ('balance_gte', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('balance_lte', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='onlinebanking.Account')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('onlinebanking.trigger',),
        ),
    ]
