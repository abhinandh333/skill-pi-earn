from allauth.account.signals import user_signed_up
from django.dispatch import receiver

@receiver(user_signed_up)
def populate_user_social_data(request, user, sociallogin=None, **kwargs):
    if sociallogin:
        data = sociallogin.account.extra_data
        user.email = data.get('email', '')
        user.full_name = data.get('name', '')
        user.save()
