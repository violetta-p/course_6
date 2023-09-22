from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView

from config import settings
from users.forms import UserForm, UserProfileForm
from users.models import User

import secrets
import string

from users.tokens import account_activation_token


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:sign_up_message')
    template_name = 'users/register.html'

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            subject = 'Activate your account.'
            current_site = get_current_site(self.request)
            message = render_to_string(
                'users/verification.html',
                {'domain': current_site,
                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                 'token': account_activation_token.make_token(user),
                 }
            )
            send_mail(
                subject=subject,
                html_message=message,
                message=user.email,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

@login_required
def generate_new_password(request):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    new_password = ''.join(secrets.choice(alphabet) for i in range(12))
    request.user.set_password(new_password)
    request.user.save()
    print(new_password)
    send_mail(
        subject='Your new password',
        html_message=new_password,
        message=request.user.email,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    return redirect(reverse('users:login'))

class EmailActivateView(View):
    def get(self, request, uidb64, token):
        """Метод активации аккаунта через email"""
        user = self.get_user(uidb64, token)
        if user is not None:
            user.is_active = True
            user.save()
            return redirect(reverse('users:success_verification'))
        else:
            return redirect(reverse('users:verification_failed'))


    @staticmethod
    def get_user(uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, ValidationError):
            user = None
        return user


class SuccessVerifView(TemplateView):
    template_name = 'users/success_verification.html'


class FailedVerifView(TemplateView):
    template_name = 'users/failed_verification.html'


class SignUpMessageView(TemplateView):
    template_name = 'users/sign_up_message.html'

