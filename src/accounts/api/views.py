from rest_framework.response import Response

from accounts.api.serializers import UserDetailSerializer
from app.views import LoginRequiredAPIView


class WhoAmIView(LoginRequiredAPIView):
    def get(self, request, *args, **kwargs):
        return Response(UserDetailSerializer(request.user).data)
