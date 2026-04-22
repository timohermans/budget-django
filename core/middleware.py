from django.contrib.auth.middleware import LoginRequiredMiddleware

class CustomLoginRequiredMiddleware(LoginRequiredMiddleware):
    """This middleware exists to exempt mozilla-django-oidc from middleware, because I use the the LoginRequiredMiddleware here :)"""
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path.startswith("/oidc/"):
            return None
        return super().process_view(request, view_func, view_args, view_kwargs)