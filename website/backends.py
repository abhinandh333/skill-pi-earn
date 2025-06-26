from django.contrib.auth.backends import BaseBackend
from website.models import CustomUser

class PhoneNumberBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, password=None):
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None
        return None
