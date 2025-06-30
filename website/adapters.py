from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse
from django.shortcuts import resolve_url
from django.shortcuts import redirect
from allauth.exceptions import ImmediateHttpResponse






class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        return resolve_url('/dashboard/')

    def save_user(self, request, user, form, commit=True):
        # Optional: Your existing custom logic for saving user data
        user = super().save_user(request, user, form, commit=False)
        # example: set custom fields
        user.full_name = form.cleaned_data.get('full_name')
        if commit:
            user.save()
        return user
    
class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin, **kwargs):
        user = sociallogin.user
        if not user.pk:  # New user
            # If you really still need profile completion
            # raise ImmediateHttpResponse(redirect(reverse('complete_profile')))
            pass


