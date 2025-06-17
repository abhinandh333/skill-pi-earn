from django import forms
from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    full_name = forms.CharField(max_length=255, label='Full Name')
    phone_number = forms.CharField(max_length=15, label='Phone Number')

    def save(self, request):
        user = super().save(request)
        user.full_name = self.cleaned_data['full_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.save()
        return user
    
class EmailLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')