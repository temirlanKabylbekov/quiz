from django.db import models
from django.db.models import Count

from answers.models import Answer
from app.models import DefaultManager, DefaultQueryset, TimestampedModel


class QuestionListQueryset(DefaultQueryset):

    def published(self):
        return self.filter(has_published=True)

    def has_at_least_one_question(self):
        return self.annotate(num_questions=Count('questions')).filter(num_questions__gte=1)

    def not_contains_only_questions_with_no_choices(self):
        questions_with_choices = Question.objects.has_choices().values_list('question_list', flat=True)
        return self.filter(id__in=questions_with_choices)

    def for_viewset(self):
        return self.published()\
                   .has_at_least_one_question()\
                   .not_contains_only_questions_with_no_choices()\
                   .order_by('created')


class QuestionList(TimestampedModel):

    objects = DefaultManager.from_queryset(QuestionListQueryset)()

    name = models.CharField(max_length=255)
    has_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_url(self):
        return f'/quiz/{self.id}/'

    def has_passed_by(self, user):
        return Answer.objects.filter(user=user, question__in=self.questions.all()).exists()

    def get_questions(self):
        for question in self.questions.iterator():
            if question.choices.count() > 1:
                yield question


class QuestionQueryset(DefaultQueryset):

    def has_choices(self):
        return self.annotate(num_choices=Count('choices')).filter(num_choices__gte=2)


class Question(TimestampedModel):

    objects = DefaultManager.from_queryset(QuestionQueryset)()

    question_list = models.ForeignKey('questions.QuestionList', on_delete=models.CASCADE, editable=False, related_name='questions', null=True)
    text = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.question_list}: {self.text}'

    class Meta:
        order_with_respect_to = 'question_list'


class QuestionChoice(TimestampedModel):

    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, editable=False, related_name='choices', null=True)
    text = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.question}: {self.text}'

    class Meta:
        order_with_respect_to = 'question'
