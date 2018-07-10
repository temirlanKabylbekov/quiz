from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework.views import APIView


class LoginRequiredAPIView(APIView):
    """Basic view that handles user authorization at the DRF level.

    Use it like any other django class-based-view.
    """
    permission_classes = [permissions.IsAuthenticated]


class LoginRequiredTemplateView(TemplateView):
    """Basic django view that handles only django built-in authorization mechanisms.

    Use it ONLY as the entry point for your frontend SPA, it it does not support authorization
    through DRF
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
