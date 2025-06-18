from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomSignupForm, EmailLoginForm
from django.contrib.auth.decorators import login_required




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


def email_login_view(request):
    form = EmailLoginForm(request.POST or None)
    error = None

    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('home')  # change to your homepage or dashboard
            else:
                error = "Invalid email or password."

    return render(request, 'email_login.html', {'form': form, 'error': error})

def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('login')
    else:
        form = CustomSignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

@login_required
def select_user_type(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        if user_type in ['employee', 'owner', 'normal']:
            request.user.user_type = user_type
            request.user.save()
            return redirect('/')  # or your app home page
    return render(request, 'select_user_type.html')