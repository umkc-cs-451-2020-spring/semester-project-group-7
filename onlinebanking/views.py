from decimal import Decimal
from datetime import datetime

from django.utils.timezone import make_aware
from django.core.validators import DecimalValidator 
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView as PasswordChangeViewBase
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, UpdateView, CreateView
from django.views.generic import ListView, DetailView
from .models import *
from .forms import *


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name='onlinebanking/home.html'
    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['accounts'] = Account.objects.filter(user=self.request.user)
        context['notification_count'] = Notification.objects.filter(user=self.request.user, read=None).count()
        return context

class AccountCreateView(LoginRequiredMixin, FormView):
    template_name = 'onlinebanking/create.html'
    form_class = AccountForm
    success_url = '/onlinebanking/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(FormView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AccountCreateView, self).get_form_kwargs()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AccountCreateView, self).get_context_data(**kwargs)
        context['accounts'] = Account.objects.filter(user=self.request.user)
        context['notification_count'] = Notification.objects.filter(user=self.request.user, read=None).count()
        context['form_name'] = 'Add an Account'
        context['button_text'] = 'Add Account'
        return context

class TransactionCreateView(LoginRequiredMixin, FormView):
    template_name = 'onlinebanking/create.html'
    form_class = TransactionForm

    def form_valid(self, form):
        account = get_object_or_404(Account, account_number=self.kwargs.get('accountid'), user=self.request.user)
        account.balance += form.instance.amount

        decimal_validator = DecimalValidator(DECIMAL_MAX, 2)
        try:
            decimal_validator(account.balance)
        except ValidationError:
            form.add_error('amount', 'Invalid amount. Account balance out of bounds.')
            return self.form_invalid(form)
        
        account.last_transaction_number += 1

        form.instance.balance = account.balance
        form.instance.transaction_number = account.last_transaction_number

        form.instance.account = account
        
        form.save()
        account.save()
        
        return super(FormView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('listAccountTransaction', kwargs={'accountid': self.kwargs.get('accountid')})

    def get_form_kwargs(self):
        kwargs = super(TransactionCreateView, self).get_form_kwargs()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(TransactionCreateView, self).get_context_data(**kwargs)
        context['accounts'] = Account.objects.filter(user=self.request.user)
        context['notification_count'] = Notification.objects.filter(user=self.request.user, read=None).count()
        context['form_name'] = 'Add a Transaction'
        context['button_text'] = 'Add Transaction'
        return context   

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    context_object_name = 'transactions'
    template_name = 'onlinebanking/transaction_list.html'

    def get_queryset(self):
        accountid = self.kwargs.get('accountid')
        queryset = super(TransactionListView, self).get_queryset()
        queryset = Transaction.objects.filter(account__account_number=accountid, account__user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TransactionListView, self).get_context_data(**kwargs)
        context['accountid'] = self.kwargs.get('accountid')
        context['accounts'] = Account.objects.filter(user=self.request.user)
        context['notification_count'] = Notification.objects.filter(user=self.request.user, read=None).count()
        return context

class TransactionTriggerCreateView(LoginRequiredMixin, FormView):
    template_name = 'onlinebanking/create.html'
    form_class = TransactionTriggerForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(FormView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('trigger')

    def get_form_kwargs(self):
        kwargs = super(TransactionTriggerCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(TransactionTriggerCreateView, self).get_context_data(**kwargs)
        context['accounts'] = Account.objects.filter(user=self.request.user)
        context['notification_count'] = Notification.objects.filter(user=self.request.user, read=None).count()
        context['form_name'] = 'Create a Transaction Trigger'
        context['button_text'] = 'Create Transaction Trigger'
        return context

class UserChangeView(LoginRequiredMixin, UpdateView):
    template_name = 'onlinebanking/profile.html'
    form_class = UserChangeForm
    model = User

    def form_valid(self, form):
        #form.save()
        return super(UpdateView, self).form_valid(form)

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super(UserChangeView, self).get_context_data(**kwargs)
        context['accounts'] = Account.objects.filter(user=self.request.user)
        context['notification_count'] = Notification.objects.filter(user=self.request.user, read=None).count()
        context['form_name'] = 'Update your user profile'
        context['button_text'] = 'Update Profile'
        return context

class PasswordChangeView(LoginRequiredMixin, PasswordChangeViewBase):
    template_name = 'onlinebanking/create.html'
    form_class = PasswordChangeForm
    
    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        return super(FormView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super(PasswordChangeView, self).get_context_data(**kwargs)
        context['accounts'] = Account.objects.filter(user=self.request.user)
        context['notification_count'] = Notification.objects.filter(user=self.request.user, read=None).count()
        context['form_name'] = 'Change your password'
        context['button_text'] = 'Change Password'
        return context

class TriggerView(LoginRequiredMixin, TemplateView):
    template_name = "onlinebanking/trigger.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts'] = Account.objects.filter(user=self.request.user)
        context['notification_count'] = Notification.objects.filter(user=self.request.user, read=None).count()

        context['user_trigger'] =  UserTrigger.objects.get(user=self.request.user)
        context['account_triggers'] = AccountTrigger.objects.filter(user=self.request.user)
        context['transaction_triggers'] = TransactionTrigger.objects.filter(user=self.request.user)
        return context

class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code=406
        return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            response = render(self.request, self.success_template_name, self.ajax_context())
        return response


class ToggleTriggerView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        trigger = get_object_or_404(Trigger, Q(pk=self.kwargs.get('pk')) & Q(Q(accounttrigger__user=self.request.user) | Q(transactiontrigger__user=self.request.user) | Q(usertrigger__user=self.request.user)))
        trigger.enabled = not trigger.enabled
        trigger.save()
        return render(self.request, 'onlinebanking/toggle_trigger.html', {
            'trigger': trigger,
        })

class TriggerCreateView(LoginRequiredMixin, AjaxableResponseMixin, CreateView):
    template_name = None
    success_view = None
    form_class = None
    model = None

    def get_form_kwargs(self):
        kwargs = super(TriggerCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class TriggerUpdateView(LoginRequiredMixin, AjaxableResponseMixin, UpdateView):
    template_name = None
    success_view = None
    form_class = None
    model = None

    def get_form_kwargs(self):
        kwargs = super(TriggerUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class UserTriggerUpdateView(TriggerUpdateView):
    template_name = 'onlinebanking/user_trigger_update.html'
    success_template_name = 'onlinebanking/user_trigger_list.html'

    form_class = UserTriggerForm
    model = UserTrigger

    def get_object(self):
        return self.model.objects.get(user=self.request.user)

    def get_success_url(self):
        return reverse('userTriggerUpdate')

    def ajax_context(self):
        return {'user_trigger': self.model.objects.get(user=self.request.user)}

class AccountTriggerUpdateView(TriggerUpdateView):
    template_name = 'onlinebanking/account_trigger_update.html'
    success_template_name = 'onlinebanking/account_trigger_list.html'

    form_class = AccountTriggerForm
    model = AccountTrigger

    def get_object(self):
        return self.model.objects.get(pk=self.kwargs.get('pk'), user=self.request.user)

    def get_success_url(self):
        return reverse('accountTriggerUpdate', kwargs={'pk': self.kwargs.get('pk')})

    def ajax_context(self):
        return {'account_triggers': self.model.objects.filter(user=self.request.user)}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs.get('pk')
        return context

class AccountTriggerCreateView(TriggerCreateView):
    template_name = 'onlinebanking/account_trigger_create.html'
    success_template_name = 'onlinebanking/account_trigger_list.html'

    form_class = AccountTriggerForm
    model = AccountTrigger

    def get_success_url(self):
        return reverse('accountTriggerCreate')

    def ajax_context(self):
        return {'account_triggers': self.model.objects.filter(user=self.request.user)}

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(AccountTriggerCreateView, self).form_valid(form)

class AccountTriggerDeleteView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        trigger = Trigger.objects.get(Q(pk=self.kwargs.get('pk')) & Q(Q(accounttrigger__user=self.request.user) | Q(transactiontrigger__user=self.request.user) | Q(usertrigger__user=self.request.user)))
        trigger.delete()
        return render(self.request, 'onlinebanking/account_trigger_list.html', {
            'account_triggers': AccountTrigger.objects.filter(user=self.request.user)
        })

class TransactionTriggerUpdateView(TriggerUpdateView):
    template_name = 'onlinebanking/transaction_trigger_update.html'
    success_template_name = 'onlinebanking/transaction_trigger_list.html'

    form_class = TransactionTriggerForm
    model = TransactionTrigger

    def get_object(self):
        return self.model.objects.get(pk=self.kwargs.get('pk'), user=self.request.user)

    def get_success_url(self):
        return reverse('transactionTriggerUpdate', kwargs={'pk': self.kwargs.get('pk')})

    def ajax_context(self):
        return {'transaction_triggers': self.model.objects.filter(user=self.request.user)}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs.get('pk')
        return context

class TransactionTriggerCreateView(TriggerCreateView):
    template_name = 'onlinebanking/transaction_trigger_create.html'
    success_template_name = 'onlinebanking/transaction_trigger_list.html'

    form_class = TransactionTriggerForm
    model = TransactionTrigger

    def get_success_url(self):
        return reverse('transactionTriggerCreate')

    def ajax_context(self):
        return {'transaction_triggers': self.model.objects.filter(user=self.request.user)}

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(TransactionTriggerCreateView, self).form_valid(form)

class TransactionTriggerDeleteView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        trigger = Trigger.objects.get(Q(pk=self.kwargs.get('pk')) & Q(Q(accounttrigger__user=self.request.user) | Q(transactiontrigger__user=self.request.user) | Q(usertrigger__user=self.request.user)))
        trigger.delete()
        return render(self.request, 'onlinebanking/transaction_trigger_list.html', {
            'transaction_triggers': TransactionTrigger.objects.filter(user=self.request.user)
        })

class NotificationDetailView(LoginRequiredMixin, DetailView):
    model = Notification

    def get(self, request, *args, **kwargs):
        notification = self.get_object()
        if notification.user != request.user:
            return HttpResponseNotFound()
        if not notification.read:
            notification.read = make_aware(datetime.now())
            notification.save()
        return super(NotificationDetailView, self).get(request, *args, **kwargs)

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    context_object_name = 'notifications'
    template_name = 'onlinebanking/notification_list.html'


    def get_queryset(self):
        queryset = super(NotificationListView, self).get_queryset()
        queryset = Notification.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(NotificationListView, self).get_context_data(**kwargs)
        context['accounts'] = Account.objects.filter(user=self.request.user)
        context['notification_count'] = Notification.objects.filter(user=self.request.user, read=None).count()
        return context