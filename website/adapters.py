from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import CustomUser


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        # This handles email/password signup
        user = super().save_user(request, user, form, commit=False)
        user.full_name = form.cleaned_data.get('full_name')
        user.phone_number = form.cleaned_data.get('phone_number')
        if commit:
            user.save()
        return user


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        # This handles Google login
        user = super().populate_user(request, sociallogin, data)
        user.full_name = data.get('name', '')
        user.email = data.get('email', '')
        return user
