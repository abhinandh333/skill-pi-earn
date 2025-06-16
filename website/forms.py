from django import forms
from .models import CustomUser
from allauth.account.forms import SignupForm
from django.core.exceptions import ValidationError

class CustomSignupForm(SignupForm):
    full_name = forms.CharField(label='Full Name')
    phone_number = forms.CharField(label='Phone Number')

    class Meta:
        model = CustomUser
        fields = ['full_name', 'phone_number']

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if CustomUser.objects.filter(phone_number=phone).exists():
            raise ValidationError("A user with this phone number already exists.")
        return phone

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return p2

    def save(self, request):
        user = super().save(request)
        user.full_name = self.cleaned_data['full_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.save()
        return user


