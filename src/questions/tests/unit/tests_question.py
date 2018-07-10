from django.test import TestCase

from app.test import Factory, mixer
from questions.models import Question


class TestHasChoicesQueryset(TestCase):

    def test_question_without_choices(self):
        question = mixer.blend('questions.Question')
        assert question not in Question.objects.has_choices()

    def test_question_with_single_choice(self):
        question = Factory.question(num_choices=1)
        assert question not in Question.objects.has_choices()

    def test_question_with_two_choices(self):
        question = Factory.question(num_choices=2)
        assert question in Question.objects.has_choices()
