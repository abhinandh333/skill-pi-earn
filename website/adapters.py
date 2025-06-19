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
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user

        # If user is already logged in or doesn't have email, skip
        if not user or not user.email:
            return

        # If the user exists, get the DB user
        from website.models import CustomUser  # update with your actual user model
        try:
            db_user = CustomUser.objects.get(email=user.email)
        except CustomUser.DoesNotExist:
            return  # first time login, nothing to do here

        # If phone number is missing, redirect to profile completion
        if not db_user.phone_number:
            request.session['socialaccount_email'] = db_user.email  # optional
            raise ImmediateHttpResponse(redirect(reverse('complete_profile')))
