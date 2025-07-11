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
    if request.GET.get('logged_out'):
        messages.info(request, "You have been logged out.")
    return render(request, 'home.html')



from django.core.mail import send_mail
from django.shortcuts import render, redirect

def contact(request):
    if request.method == "POST":
        message = request.POST['message']
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']

        full_message = f"Message from {name} <{email}>:\n\n{message}"

        send_mail(
            subject,
            full_message,
            email,
            ['skillpiearn333@gmail.com'],  # Replace with your email
            fail_silently=False,
        )

        # Store name in session to show thank you message
        request.session['contact_name'] = name
        return redirect('contact')  # Redirect to same page (GET method)

    name = request.session.pop('contact_name', None)  # Get and remove from session
    return render(request, 'contact.html', {'name': name})

    
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
from django.shortcuts import render
from .forms import SearchForm
from .models import Profile

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
        else:
            # If category is 'all', don't show any results
            results = results.none()
            messages.warning(request, "⚠️ Work category is required to filter results.")

    # ✅ Always return a response
    return render(request, "search_results.html", {
        "form": form,
        "results": results
    })



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



def profile_detail(request, user_id):
    profile = get_object_or_404(Profile, user__id=user_id)
    return render(request, 'profile_detail.html', {'profile': profile})


def job_listing(request):
    return render(request, 'job_listing.html')


from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, Review
from .forms import ReviewForm

@login_required
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



from django.http import HttpResponse

def robots_txt(request):
    content = (
        "User-agent: *\n"
        "Disallow:\n"
        "Sitemap: https://www.skillpiearn.com/sitemap.xml"
    )
    return HttpResponse(content, content_type="text/plain")




from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import WorkerProfile, CustomUser

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterTelegramSerializer
from django.views.decorators.csrf import csrf_exempt



@api_view(['POST'])
@csrf_exempt
def telegram_register(request):
    serializer = RegisterTelegramSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # 🔁 Ensure WorkerProfile exists (create if missing)
        if not WorkerProfile.objects.filter(user=user).exists():
            WorkerProfile.objects.create(
                user=user,
                full_name=user.full_name,
                category=request.data.get('category', ''),
                city=request.data.get('city', ''),
                district=request.data.get('district', ''),
                state=request.data.get('state', ''),
            )

        return Response({"message": "Registered successfully ✅"}, status=200)
    else:
        print("❌ Invalid Data Received:")
        print(request.data)
        print("❌ Serializer Errors:")
        print(serializer.errors)
        return Response(serializer.errors, status=400)



# website/views.py
from .models import WorkerProfile
from rest_framework import serializers

class WorkerProfileSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerProfile
        fields = ['full_name', 'phone_number', 'city', 'district', 'state', 'category', 'description']

@api_view(['GET'])
def search_profiles(request):
    category = request.GET.get('category', '').strip().lower()
    city = request.GET.get('city', '').strip().lower()
    district = request.GET.get('district', '').strip().lower()

    qs = WorkerProfile.objects.all()

    if city:
        qs = qs.filter(city__iexact=city)
    elif district:
        qs = qs.filter(district__iexact=district)

    if category:
        qs = qs.filter(category__iexact=category)

    results = qs[:2]  # Limit to 2

    serializer = WorkerProfileSearchSerializer(results, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def my_profile(request, telegram_user_id):
    try:
        user = CustomUser.objects.get(telegram_user_id=telegram_user_id)
        profile = WorkerProfile.objects.get(user=user)
        serializer = WorkerProfileSearchSerializer(profile)
        return Response(serializer.data)
    except:
        return Response({"error": "Profile not found"}, status=404)

