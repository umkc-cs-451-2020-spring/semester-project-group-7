from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth import views as auth_views
from django.contrib.auth import login as auth_login
from .forms import LoginForm, RegisterForm

"""
class HomePageView(TemplateView):
    template_name = "commercebank/home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #messages.info(self.request, "hello http://example.com")
        return context
        """

class LoginView(auth_views.LoginView):
    form_class = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']  # get remember me data from cleaned_data of form
        if not remember_me:
            self.request.session.set_expiry(0)  # if remember me is 
            self.request.session.modified = True
        return super(LoginView, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        response = super(LoginView, self).dispatch(*args, **kwargs)
        response['x-login'] = reverse('login')
        return response

class UserRegistrationdView(FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        form.save()
        return super(FormView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')

class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset.html'
    form_class = PasswordResetForm
    
    def get_success_url(self):
        return reverse_lazy('passwordResetDone')


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    
    def get_success_url(self):
        return reverse_lazy('passwordResetComplete')

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
