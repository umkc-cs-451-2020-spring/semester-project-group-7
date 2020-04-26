from django.urls import path
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from .views import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('account/create', AccountCreateView.as_view(), name='accountCreate'),
    path('account/<int:accountid>/transactions/add/', TransactionCreateView.as_view(), name='addAccountTransaction'),
    path('account/<int:accountid>/transactions/', TransactionListView.as_view(), name='listAccountTransaction'),
    
    path('trigger/', TriggerView.as_view(), name='trigger'),
    path('trigger/<pk>/toggle', ToggleTriggerView.as_view(), name='toggleTrigger'),
    
    path('trigger/user/update', UserTriggerUpdateView.as_view(), name='userTriggerUpdate'),
    
    path('trigger/account/<pk>/update', AccountTriggerUpdateView.as_view(), name='accountTriggerUpdate'),
    path('trigger/account/<pk>/delete', AccountTriggerDeleteView.as_view(), name='accountTriggerDelete'),
    path('trigger/account/create', AccountTriggerCreateView.as_view(), name='accountTriggerCreate'),

    path('trigger/transaction/<pk>/update', TransactionTriggerUpdateView.as_view(), name='transactionTriggerUpdate'),
    path('trigger/transaction/<pk>/delete', TransactionTriggerDeleteView.as_view(), name='transactionTriggerDelete'),
    path('trigger/transaction/create', TransactionTriggerCreateView.as_view(), name='transactionTriggerCreate'),

    path('notification/', NotificationListView.as_view(), name='notificationList'),
    path('notification/<pk>/', NotificationDetailView.as_view(), name='notificationDetail'),
    
    path('profile/', UserChangeView.as_view(), name='profile'),
    path('profile/change_pass', PasswordChangeView.as_view(), name='passwordChange'),
]