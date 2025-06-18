from django.shortcuts import redirect

class ForceUserTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            request.user.is_authenticated and
            not request.user.is_superuser and
            not request.user.is_staff and
            not request.user.user_type and
            request.path != '/select-user-type/' and
            not request.path.startswith('/admin/') and
            not request.path.startswith('/accounts/logout/')
        ):
            return redirect('/select-user-type/')
        return self.get_response(request)
