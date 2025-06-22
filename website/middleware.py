from django.shortcuts import redirect

class ForceUserTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated and not user.is_superuser and not user.is_staff:
            # Force selection of user_type
            if (
                not user.user_type and
                request.path != '/select-user-type/' and
                not request.path.startswith('/admin/') and
                not request.path.startswith('/accounts/logout/')
            ):
                return redirect('/select-user-type/')

            # Force profile completion if user is "owner"
            elif (
                user.user_type == 'owner' and
                not hasattr(user, 'profile') and  # assuming Profile model is OneToOne with user
                request.path != '/complete-profile/' and
                not request.path.startswith('/admin/') and
                not request.path.startswith('/accounts/logout/')
            ):
                return redirect('/dashboard/')

        return self.get_response(request)
    



from django.http import HttpResponsePermanentRedirect

class WWWRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        if host == 'skillpiearn.com':
            return HttpResponsePermanentRedirect(
                f"https://www.skillpiearn.com{request.get_full_path()}"
            )
        return self.get_response(request)

