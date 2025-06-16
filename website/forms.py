from django import forms
from .models import CustomUser
from allauth.account.forms import SignupForm
from django import forms



class CustomSignupForm(SignupForm):
    full_name = forms.CharField(label='Full Name')
    phone_number = forms.CharField(label='Phone Number')

    def save(self, request):
        user = super().save(request)
        user.full_name = self.cleaned_data['full_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.save()
        return user


    class Meta:
        model = CustomUser
        fields = ['full_name', 'phone_number']  # ✅ include full_name here

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        return p2

   
