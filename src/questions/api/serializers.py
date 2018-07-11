from rest_framework import serializers

from questions.models import Question, QuestionChoice, QuestionList


class QuestionListFastSerializer(serializers.ModelSerializer):

    passed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = QuestionList
        fields = [
            'id',
            'name',
            'passed',
        ]

    def get_passed(self, obj):
        return obj.has_passed_by(self.context['request'].user)


class QuestionListSerializer(QuestionListFastSerializer):

    url = serializers.CharField(source='get_url', read_only=True)

    class Meta(QuestionListFastSerializer.Meta):
        fields = QuestionListFastSerializer.Meta.fields + ['url', 'created']


class QuestionListDetailSerializer(QuestionListFastSerializer):

    questions = serializers.SerializerMethodField(read_only=True)

    class Meta(QuestionListFastSerializer.Meta):
        fields = QuestionListFastSerializer.Meta.fields + ['questions']

    def get_questions(self, obj):
        return QuestionSerializer(obj.get_questions(), many=True).data


class QuestionChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionChoice
        fields = [
            'id',
            'text',
        ]


class QuestionSerializer(serializers.ModelSerializer):

    choices = QuestionChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            'id',
            'text',
            'choices',
        ]


class QuestionAnswerStats(serializers.ModelSerializer):

    question_id = serializers.IntegerField(source='id')
    stats = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Question
        fields = [
            'question_id',
            'stats',
        ]

    def get_stats(self, obj):
        return list(obj.get_choices_percentage())
