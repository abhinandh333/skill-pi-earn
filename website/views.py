from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def contact(request):
    if request.method == "POST":
        message = request.POST['message']
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']

        context = {
            'message': message,
            'name': name,
            'email': email,
            'subject': subject,
        }

        return render(request, 'contact.html', context)


    else:
        return render(request, 'contact.html')
    
def about(request):
    return render(request, 'about.html')



def base(request):
    return render(request, 'base.html')

def joblist(request):
    return render(request, 'joblist.html')

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomSignupForm



def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save(request)
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')  # Redirect to login page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomSignupForm()
    
    return render(request, 'signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        user = authenticate(request, phone_number=phone_number, password=password)

        if user is not None:
            login(request, user)  # ✅ Correct call
            return redirect('home')
        else:
            messages.error(request, 'Invalid phone number or password')

    return render(request, 'login.html')

