from django import forms
from allauth.account.forms import SignupForm
from .models import Profile, ProductImage

class CustomSignupForm(SignupForm):
    full_name = forms.CharField(max_length=255, label='Full Name')
    phone_number = forms.CharField(max_length=15, label='Phone Number')
    date_of_birth = forms.DateField(
        label='Date of Birth',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def save(self, request):
        user = super().save(request)
        user.full_name = self.cleaned_data['full_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.save()
        return user
    
class EmailLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    STATE_CHOICES = [
        ('Kerala', 'Kerala'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Karnataka', 'Karnataka'),
        # Add all states here
    ]

    KERALA_DISTRICT_CHOICES = [
    ("Thiruvananthapuram", "Thiruvananthapuram"),
    ("Kollam", "Kollam"),
    ("Pathanamthitta", "Pathanamthitta"),
    ("Alappuzha", "Alappuzha"),
    ("Kottayam", "Kottayam"),
    ("Idukki", "Idukki"),
    ("Ernakulam", "Ernakulam"),
    ("Thrissur", "Thrissur"),
    ("Palakkad", "Palakkad"),
    ("Malappuram", "Malappuram"),
    ("Kozhikode", "Kozhikode"),
    ("Wayanad", "Wayanad"),
    ("Kannur", "Kannur"),
    ("Kasaragod", "Kasaragod"),
]

    state = forms.ChoiceField(choices=STATE_CHOICES, required=True)
    district = forms.ChoiceField(choices=KERALA_DISTRICT_CHOICES, required=True)

    class Meta:
        model = Profile
        fields = [
            'full_name',
            'phone_number',
            'alternate_phone',
            'date_of_birth',
            'user_type',
            'alt_number',
            'state',
            'district',
            'city',
            'category',
            'profile_picture',
            'product_image',
           ]


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']


from django import forms
from .models import Profile  # or your actual profile model

STATE_CHOICES = [
    ('Kerala', 'Kerala'),
    ('Tamil Nadu', 'Tamil Nadu'),
]

KERALA_DISTRICT_CHOICES = [
    ('Thiruvananthapuram', 'Thiruvananthapuram'),
    ('Kollam', 'Kollam'),
    ('Pathanamthitta', 'Pathanamthitta'),
    ('Alappuzha', 'Alappuzha'),
    ('Kottayam', 'Kottayam'),
    ('Idukki', 'Idukki'),
    ('Ernakulam', 'Ernakulam'),
    ('Thrissur', 'Thrissur'),
    ('Palakkad', 'Palakkad'),
    ('Malappuram', 'Malappuram'),
    ('Kozhikode', 'Kozhikode'),
    ('Wayanad', 'Wayanad'),
    ('Kannur', 'Kannur'),
    ('Kasaragod', 'Kasaragod'),
]


class ProfileEditForm(forms.ModelForm):
    state = forms.ChoiceField(choices=STATE_CHOICES, required=True)
    district = forms.ChoiceField(choices=KERALA_DISTRICT_CHOICES, required=True)
    USER_TYPE_CHOICES = [
        ('employee', 'Employee'),
        ('shop_owner', 'Shop/Enterprise Owner'),
        ('normal_user', 'normal user')
    ]
    user_type = forms.ChoiceField(choices=Profile.USER_TYPE_CHOICES,required=True)

    class Meta:
        model = Profile
        fields = [
            'full_name',
            'phone_number',
            'alternate_phone',
            'date_of_birth',
            'user_type',
            'description',
            'state',
            'district',
            'city',
            'category',
            'profile_picture',
            'product_image'
        ]

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
from django import forms
from .models import Profile  # Replace with your model

STATE_CHOICES = [('All', 'All'), ('Kerala', 'Kerala')]
DISTRICT_CHOICES = [('All', 'All'), ('Kottayam', 'Kottayam')]
CITY_CHOICES = [('All', 'All'), ('Changanacherry', 'Changanacherry')]
CATEGORY_CHOICES = [
    ('All', 'All'),
    ('driver', 'Driver'),
    ('carpenter', 'Carpenter'),
    ('plumber', 'Plumber'),
    ('electrician', 'Electrician'),
    ('it tech', 'IT Tech'),
]

class SearchForm(forms.Form):
    state = forms.ChoiceField(choices=STATE_CHOICES)
    district = forms.ChoiceField(choices=DISTRICT_CHOICES)
    city = forms.CharField(required=False)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
        # Specific styling for select fields
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'w-full p-2 border border-gray-500 rounded bg-gray-800 text-white'
                    
                })
            else:
             # Generic styling for input fields like city
                field.widget.attrs.update({
                    'class': 'w-full p-2 border border-gray-500 rounded bg-gray-700 text-white'
                })



from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': '0',
                'max': '5',
                'step': '0.5',
                'class': 'form-control',
                'placeholder': 'Rate out of 5',
            }),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }







