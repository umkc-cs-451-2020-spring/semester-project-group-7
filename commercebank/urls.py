"""commercebank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls as auth_urls
from django.urls import include, path

from .views import *

urlpatterns = [
    path('', LoginView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='passwordResetConfirm'),
    path('reset/sent/', PasswordResetDoneView.as_view(), name='passwordResetDone'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='passwordResetComplete'),
    path('reset/', PasswordResetView.as_view(), name='passwordReset'),
    path('', include(auth_urls)),
    path('register/', UserRegistrationdView.as_view(), name='register'),
    path('onlinebanking/', include('onlinebanking.urls')),
    path('admin/', admin.site.urls),
]