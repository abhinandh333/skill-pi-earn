from django.shortcuts import redirect
from django.urls import resolve, Resolver404


# middleware.py
from django.urls import resolve, Resolver404




class CompleteProfileRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        safe_paths = ['complete_profile', 'logout', 'login', 'account_login', 'account_signup', 'socialaccount_signup']


        if request.user.is_authenticated:
            try:
                current_url_name = resolve(request.path_info).url_name
            except Resolver404:
                current_url_name = None

            if not request.user.phone_number and current_url_name not in safe_paths:
                return redirect('complete_profile')

        return self.get_response(request)

