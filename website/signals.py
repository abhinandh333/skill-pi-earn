from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from allauth.account.signals import user_signed_up
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile


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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)