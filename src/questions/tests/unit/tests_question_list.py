from django.test import TestCase

from app.test import Factory, mixer
from questions.models import QuestionList


class TestHasAtLeastOneQuestionQueryset(TestCase):

    def test_not_contains_empty_list(self):
        empty_list = mixer.blend('questions.QuestionList')
        assert empty_list not in QuestionList.objects.has_at_least_one_question()

    def test_contains_list_with_single_question(self):
        list_with_one_question = mixer.blend('questions.QuestionList')
        mixer.blend('questions.Question', question_list=list_with_one_question)
        assert list_with_one_question in QuestionList.objects.has_at_least_one_question()

    def test_contains_list_with_more_than_one_question(self):
        list_with_two_questions = mixer.blend('questions.QuestionList')
        mixer.cycle(2).blend('questions.Question', question_list=list_with_two_questions)
        assert list_with_two_questions in QuestionList.objects.has_at_least_one_question()


class TestNotContainsOnlyQuestionsWithNoChoicesQueryset(TestCase):

    def test_not_contains_question_with_zero_choices(self):
        question_list = mixer.blend('questions.QuestionList')
        mixer.blend('questions.Question', question_list=question_list)
        assert question_list not in QuestionList.objects.not_contains_only_questions_with_no_choices()

    def test_not_contains_question_with_single_choice(self):
        question_list = mixer.blend('questions.QuestionList')
        question = mixer.blend('questions.Question', question_list=question_list)
        mixer.blend('questions.QuestionChoice', question=question)
        assert question_list not in QuestionList.objects.not_contains_only_questions_with_no_choices()

    def test_contains_question_with_two_choices(self):
        question_list = mixer.blend('questions.QuestionList')
        question = mixer.blend('questions.Question', question_list=question_list)
        mixer.cycle(2).blend('questions.QuestionChoice', question=question)
        assert question_list in QuestionList.objects.not_contains_only_questions_with_no_choices()


class TestHasPassedByMethod(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = mixer.blend('auth.User')

    def test_given_user_answered_questions_in_list(self):
        question_list = Factory.question_list(num_questions=2, num_choices=3)
        question_list = Factory.answered_question_list(question_list, self.user)
        assert question_list.has_passed_by(self.user) is True

    def test_given_user_not_answer_on_any_questions_in_list(self):
        question_list = Factory.question_list(num_questions=2, num_choices=2)
        assert question_list.has_passed_by(self.user) is False

    def test_list_not_contains_questions(self):
        question_list = mixer.blend('questions.QuestionList')
        assert question_list.has_passed_by(self.user) is False


class TestGetQuestionsMethod(TestCase):

    def test_not_contains_question_with_no_choices(self):
        qlist = mixer.blend('questions.QuestionList')
        question = Factory.question(num_choices=0, question_list=qlist)
        assert question not in qlist.get_questions()

    def test_not_contains_question_with_single_choice(self):
        qlist = mixer.blend('questions.QuestionList')
        question = Factory.question(num_choices=1, question_list=qlist)
        assert question not in qlist.get_questions()

    def test_keeping_order(self):
        qlist = mixer.blend('questions.QuestionList')
        q1 = Factory.question(num_choices=2, question_list=qlist)
        q2 = Factory.question(num_choices=0, question_list=qlist)
        q3 = Factory.question(num_choices=3, question_list=qlist)
        q4 = Factory.question(num_choices=1, question_list=qlist)
        q5 = Factory.question(num_choices=2, question_list=qlist)
        qlist.set_question_order([q1.id, q5.id, q3.id, q4.id, q2.id])

        assert list(qlist.get_questions()) == [q1, q5, q3]
