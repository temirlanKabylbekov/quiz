from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.api.views import MultiSerializerMixin
from questions.api import serializers
from questions.models import QuestionList


class QuestionListViewset(MultiSerializerMixin, viewsets.ModelViewSet):

    queryset = QuestionList.objects.for_viewset()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.QuestionListSerializer
    serializer_action_classes = {
        'retrieve': serializers.QuestionListDetailSerializer,
    }
