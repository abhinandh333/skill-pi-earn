# website/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('home/', views.home, name='home'),
    path('base/', views.base, name='base'),
    path('joblist/', views.joblist, name='joblist'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
]

