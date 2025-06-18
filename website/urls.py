# website/urls.py
from django.urls import path,include
from . import views
from .views import email_login_view
from django.conf import settings
from django.conf.urls.static import static
from .views import select_user_type

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
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

