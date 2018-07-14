from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

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

    name = models.CharField(_('Question list name'), max_length=255)
    has_published = models.BooleanField(_('To publsish'), default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Question list')
        verbose_name_plural = _('Question lists')

    def get_url(self):
        return f'/quiz/{self.id}/'

    def has_passed_by(self, user):
        return Answer.objects.filter(user=user, question__in=self.questions.all()).exists()

    def get_questions(self):
        for question in self.questions.iterator():
            if question.choices.count() > 1:
                yield question

    def set_answers(self, user, answers):
        if self.has_passed_by(user) is True:
            raise ValidationError('the same user can`t answer on quiz twice')

        accepted_question_ids = sorted([answer['question'] for answer in answers])
        question_ids = sorted([question.id for question in self.get_questions()])
        if accepted_question_ids != question_ids:
            raise ValidationError('passed invalid question_id or not all the answers to the questions sent')

        for answer in answers:
            if QuestionChoice.objects.filter(question_id=answer['question'], id=answer['choice']).exists() is False:
                raise ValidationError('passed invalid choice_id')

        Answer.objects.bulk_create([
            Answer(user=user, question_id=answer['question'], choice_id=answer['choice']) for answer in answers
        ])


class QuestionQueryset(DefaultQueryset):

    def has_choices(self):
        return self.annotate(num_choices=Count('choices')).filter(num_choices__gte=2)


class Question(TimestampedModel):

    objects = DefaultManager.from_queryset(QuestionQueryset)()

    question_list = models.ForeignKey('questions.QuestionList', on_delete=models.CASCADE, editable=False, related_name='questions', null=True)
    text = models.CharField(_('Question text'), max_length=255)

    def __str__(self):
        return f'{self.question_list}: {self.text}'

    class Meta:
        order_with_respect_to = 'question_list'
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    def get_answer_for_user(self, user):
        return Answer.objects.filter(question=self, user=user).first()

    def get_choices_percentage(self):
        answers = Answer.objects.filter(question=self).values('choice').annotate(Count('user'))
        num_question_answers = sum([answer['user__count'] for answer in answers])

        for choice in self.choices.iterator():
            choice_answers = next((answer['user__count'] for answer in answers if answer['choice'] == choice.id), 0)
            percent = 0 if num_question_answers == 0 else round(choice_answers / num_question_answers * 100)
            yield {
                'choice': choice.id,
                'percent': percent,
            }


class QuestionChoice(TimestampedModel):

    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, editable=False, related_name='choices', null=True)
    text = models.CharField(_('Question choice text'), max_length=255)

    def __str__(self):
        return f'{self.question}: {self.text}'

    class Meta:
        order_with_respect_to = 'question'
        verbose_name = _('Question choice')
        verbose_name_plural = _('Question choices')
