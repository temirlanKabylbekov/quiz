import json

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError
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

    @detail_route(methods=['post'], permission_classes=[IsAuthenticated])
    def set_answers(self, request, pk=None):
        instance = self.get_object()
        print(request.data, type(request.data['answers']))
        try:
            instance.set_answers(request.user, json.loads(request.data['answers']))
        except DjangoValidationError as e:
            raise ValidationError(e.message)

        return Response(status=status.HTTP_200_OK)
