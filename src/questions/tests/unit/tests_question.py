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


class TestGetChoicesPercentageMethod(TestCase):

    def test_question_without_choices(self):
        question = mixer.blend('questions.Question')
        assert list(question.get_choices_percentage()) == []

    def test_question_with_not_selected_single_choice(self):
        question = mixer.blend('questions.Question')
        choice = mixer.blend('questions.QuestionChoice', question=question)
        assert list(question.get_choices_percentage()) == [{'choice': choice.id, 'percent': 0}]

    def test_not_selected_by_any_user_question_choices(self):
        question = mixer.blend('questions.Question')
        choice1 = mixer.blend('questions.QuestionChoice', question=question)
        choice2 = mixer.blend('questions.QuestionChoice', question=question)
        assert list(question.get_choices_percentage()) == [
            {'choice': choice1.id, 'percent': 0},
            {'choice': choice2.id, 'percent': 0},
        ]

    def test_only_one_choice_was_selected(self):
        question = mixer.blend('questions.Question')
        choice1 = mixer.blend('questions.QuestionChoice', question=question)
        choice2 = mixer.blend('questions.QuestionChoice', question=question)
        Factory.answered_question_choice(choice1, num_answers=2)
        assert list(question.get_choices_percentage()) == [
            {'choice': choice1.id, 'percent': 100},
            {'choice': choice2.id, 'percent': 0},
        ]

    def _create_question_with_answers(self, answers):
        question = mixer.blend('questions.Question')
        choice1 = mixer.blend('questions.QuestionChoice', question=question)
        choice2 = mixer.blend('questions.QuestionChoice', question=question)
        choice3 = mixer.blend('questions.QuestionChoice', question=question)
        Factory.answered_question_choice(choice1, num_answers=answers[0])
        Factory.answered_question_choice(choice2, num_answers=answers[1])
        Factory.answered_question_choice(choice3, num_answers=answers[2])
        return question, choice1, choice2, choice3

    def test_fractional_percentage_1(self):
        question, choice1, choice2, choice3 = self._create_question_with_answers([1, 1, 1])
        assert list(question.get_choices_percentage()) == [
            {'choice': choice1.id, 'percent': 33},
            {'choice': choice2.id, 'percent': 33},
            {'choice': choice3.id, 'percent': 33},
        ]

    def test_fractional_percentage_2(self):
        question, choice1, choice2, choice3 = self._create_question_with_answers([1, 2, 3])
        assert list(question.get_choices_percentage()) == [
            {'choice': choice1.id, 'percent': 17},
            {'choice': choice2.id, 'percent': 33},
            {'choice': choice3.id, 'percent': 50},
        ]

    def test_fractional_percentage_3(self):
        question, choice1, choice2, choice3 = self._create_question_with_answers([1, 2, 0])
        assert list(question.get_choices_percentage()) == [
            {'choice': choice1.id, 'percent': 33},
            {'choice': choice2.id, 'percent': 67},
            {'choice': choice3.id, 'percent': 0},
        ]

    def test_fractional_percentage_4(self):
        question, choice1, choice2, choice3 = self._create_question_with_answers([4, 4, 0])
        assert list(question.get_choices_percentage()) == [
            {'choice': choice1.id, 'percent': 50},
            {'choice': choice2.id, 'percent': 50},
            {'choice': choice3.id, 'percent': 0},
        ]
