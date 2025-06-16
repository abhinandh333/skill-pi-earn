from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import CustomUser

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        # This method is called before the user is saved.
        user = super().populate_user(request, sociallogin, data)
        user.full_name = data.get('name', '')
        user.email = data.get('email', '')
        return user
