from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

    @detail_route(methods=['get'], permission_classes=[IsAuthenticated])
    def answer_stats(self, request, pk=None):
        instance = self.get_object()
        return Response(serializers.QuestionAnswerStats(instance.get_questions(), many=True).data)
