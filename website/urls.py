# website/urls.py
from django.urls import path,include
from . import views
from .views import email_login_view
from django.conf import settings
from django.conf.urls.static import static
from .views import select_user_type
from .views import location_filter_view,dashboard
from .views import edit_profile
from django.contrib.auth.views import LogoutView
from django.urls import path
from website.views import robots_txt
from django.urls import path
from .views import telegram_register, search_profiles, my_profile


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('home/', views.home, name='home'),
    path('base/', views.base, name='base'),
    path('joblist/', views.joblist, name='joblist'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('accounts/', include('allauth.urls')),
    path('select-user-type/', select_user_type, name='select_user_type'),
    
    path('search/', views.search_employees, name='search_employees'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/<int:user_id>/', views.profile_detail, name='profile_detail'),
    path('review/<int:user_id>/', views.submit_review, name='submit_review'),
    path('job_listing/', views.job_listing, name='job_listing'),
    path('logout/', LogoutView.as_view(next_page='/?logged_out=1'), name='logout'),
    path("robots.txt", robots_txt, name="robots_txt"),
    path('api/telegram-register/', telegram_register, name='telegram_register'),
    path('api/my-profile/<int:telegram_user_id>/', my_profile, name='my_profile'),
    path('api/search-profiles/', search_profiles, name='search_profiles'),


]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

