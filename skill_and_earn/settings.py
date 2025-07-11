"""
Django settings for skill_and_earn project.
"""

import os
from pathlib import Path
import dj_database_url  # ✅ Import moved to top
from allauth.core.exceptions import ImmediateHttpResponse

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-t4qd!)n0gr8xa=@f#4n*ik_nzrfm#)=set$31u#x(so#ys3n+p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*'
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'website',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'widget_tweaks',
    'django.contrib.sitemaps',
    'rest_framework',
    

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ Correct place
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
   
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    

  
]

SITE_ID = 1



AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]



LOGOUT_REDIRECT_URL = 'select_user_type'

ROOT_URLCONF = 'skill_and_earn.urls'

import os
from decouple import config




 

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
WSGI_APPLICATION = 'skill_and_earn.wsgi.application'


# ✅ Use dj_database_url directly without defining DATABASES twice
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 6},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'

AUTH_USER_MODEL = 'website.CustomUser'

ACCOUNT_ADAPTER = 'website.adapters.CustomAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'website.adapters.CustomSocialAccountAdapter'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]




# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]




STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]


SOCIALACCOUNT_ADAPTER = 'website.adapters.CustomSocialAccountAdapter'
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_LOGIN_METHODS = {'email'}  # allows login via email
LOGIN_REDIRECT_URL = '/dashboard/'
  # or wherever you want after login

ACCOUNT_FORMS = {
    'signup': 'website.forms.CustomSignupForm'
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'skillpiearn333@gmail.com'
EMAIL_HOST_PASSWORD = 'tdhq yblc xlwp lqog'  # use App Password, NOT your Gmail password

DEFAULT_FROM_EMAIL = 'Skill And Earn <skillpiearn333@gmail.com>'




MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# settings.py
LOGIN_URL = '/accounts/login/'

CSRF_TRUSTED_ORIGINS = [
    "https://skillpiearn.com",
    "https://www.skillpiearn.com",
    # If using www version too, include this:
    # "https://www.skillpiearn.com",
]


ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http" if DEBUG else "https"






