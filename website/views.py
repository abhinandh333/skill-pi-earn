from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomSignupForm, EmailLoginForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, ProductImageForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from .models import Profile, ProductImage
from django.shortcuts import resolve_url
from .forms import ProfileEditForm





# Create your views here.from django.shortcuts import render

def home(request):
    messages.info(request, "You have been logged out.")
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
                return redirect('dashboard')  # change to your homepage or dashboard
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
            return redirect('dashboard')
    return render(request, 'login.html')

@login_required
def select_user_type(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        if user_type in ['employee', 'owner', 'normal']:
            request.user.user_type = user_type
            request.user.save()
            return redirect('dashboard')  # or your app home page
    return render(request, 'select_user_type.html')


# views.py
@login_required
def complete_profile(request):
    user = request.user

    # ✅ Get the existing profile or create one if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # replace with your actual success URL
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'complete_profile.html', {'form': form})


from django.shortcuts import render
from .models import Profile
from .forms import SearchForm

from .models import Profile
from django.db.models import Q

from django.shortcuts import render
from .models import Profile
from .forms import SearchForm

def search_employees(request):
    form = SearchForm(request.GET or None)
    results = []

    if request.GET.get("state") or request.GET.get("district") or request.GET.get("city") or request.GET.get("category"):
        state = request.GET.get("state", "").strip().lower()
        district = request.GET.get("district", "").strip().lower()
        city = request.GET.get("city", "").strip().lower()
        category = request.GET.get("category", "").strip().lower()

        results = Profile.objects.all()

        if state != "all":
            results = results.filter(state__icontains=state)
        if district != "all":
            results = results.filter(district__icontains=district)
        if city != "all":
            results = results.filter(city__icontains=city)
        if category != "all":
            results = results.filter(category__icontains=category)

    return render(request, 'search_results.html', {'form': form, 'results': results})




def location_filter_view(request):
    return render(request, 'location_filter.html')

@login_required
def dashboard(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None
    return render(request, 'dashboard.html', {'profile': profile})

def get_login_redirect_url(self, request):
    print("✅ REDIRECTING MANUAL LOGIN TO DASHBOARD")
    return resolve_url('/dashboard/')

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileEditForm(instance=profile)  # ✅ FIXED: Removed POST & FILES

    return render(request, 'edit_profile.html', {'form': form})


from django.shortcuts import render, get_object_or_404
from .models import Profile

from .models import Profile, Review

from django.shortcuts import get_object_or_404, render
from website.models import Profile, Review


@login_required
def profile_detail(request, user_id):
    profile = get_object_or_404(Profile, user__id=user_id)
    return render(request, 'profile_detail.html', {'profile': profile})


def job_listing(request):
    return render(request, 'job_listing.html')


from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, Review
from .forms import ReviewForm

def submit_review(request, user_id):
    profile = get_object_or_404(Profile, user__id=user_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.profile = profile
            review.save()
            return redirect('profile_detail', user_id=profile.user.id)
    else:
        form = ReviewForm()

    return render(request, 'submit_review.html', {'form': form, 'profile': profile})


