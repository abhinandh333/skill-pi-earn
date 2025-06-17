from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from allauth.account.signals import user_signed_up


@receiver(user_signed_up)
def populate_user_social_data(request, user, sociallogin=None, **kwargs):
    if sociallogin:
        data = sociallogin.account.extra_data
        user.email = data.get('email', '')
        user.full_name = data.get('name', '')
        user.save()


@receiver(user_logged_in)
def redirect_if_profile_incomplete(request, user, **kwargs):
    if not user.phone_number:
        request.session['redirect_to_complete_profile'] = True