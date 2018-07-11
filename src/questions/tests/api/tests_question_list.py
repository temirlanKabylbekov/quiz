import json

from answers.models import Answer
from app.test import ApiTestCase, Factory, status


class TestSetQuestionListAnswers(ApiTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.question_list = Factory.question_list(num_questions=3, num_choices=4)
        cls.questions = cls.question_list.questions.all()

    def _get_random_choice_id(self, question):
        return question.choices.order_by('?').first().id

    def test_passing_invalid_question_id(self):
        response = self.c.post(f'/api/v1/question_list/{self.question_list.id}/set_answers/', {
            'answers': json.dumps([
                {'question': 100500, 'choice': self._get_random_choice_id(self.questions[0])},
                {'question': self.questions[1].id, 'choice': self._get_random_choice_id(self.questions[1])},
                {'question': self.questions[2].id, 'choice': self._get_random_choice_id(self.questions[2])},
            ])
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == ['passed invalid question_id or not all the answers to the questions sent']

    def test_passing_invalid_count_of_questions(self):
        response = self.c.post(f'/api/v1/question_list/{self.question_list.id}/set_answers/', {
            'answers': json.dumps([
                {'question': self.questions[1].id, 'choice': self._get_random_choice_id(self.questions[1])},
                {'question': self.questions[2].id, 'choice': self._get_random_choice_id(self.questions[2])},
            ])
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == ['passed invalid question_id or not all the answers to the questions sent']

    def test_passing_invalid_choice_id(self):
        response = self.c.post(f'/api/v1/question_list/{self.question_list.id}/set_answers/', {
            'answers': json.dumps([
                {'question': self.questions[0].id, 'choice': 100500},
                {'question': self.questions[1].id, 'choice': self._get_random_choice_id(self.questions[1])},
                {'question': self.questions[2].id, 'choice': self._get_random_choice_id(self.questions[2])},
            ])
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == ['passed invalid choice_id']

    def test_setting_answer_on_question_by_the_same_user_second_time(self):
        question_list = Factory.question_list(num_questions=3, num_choices=4)
        question_list = Factory.answered_question_list(question_list, self.user)
        questions = question_list.questions.all()

        response = self.c.post(f'/api/v1/question_list/{question_list.id}/set_answers/', {
            'answers': json.dumps([
                {'question': questions[0].id, 'choice': self._get_random_choice_id(questions[0])},
                {'question': questions[1].id, 'choice': self._get_random_choice_id(questions[1])},
                {'question': questions[2].id, 'choice': self._get_random_choice_id(questions[2])},
            ])
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == ['the same user can`t answer on quiz twice']

    def test_setting_answers(self):
        question_list = Factory.question_list(num_questions=3, num_choices=4)
        questions = question_list.questions.all()
        choices = [self._get_random_choice_id(question) for question in questions]

        response = self.c.post(f'/api/v1/question_list/{question_list.id}/set_answers/', {
            'answers': json.dumps([
                {'question': questions[0].id, 'choice': choices[0]},
                {'question': questions[1].id, 'choice': choices[1]},
                {'question': questions[2].id, 'choice': choices[2]},
            ])
        })

        assert response.status_code == status.HTTP_200_OK

        assert Answer.objects.filter(user=self.user, question=questions[0], choice_id=choices[0]).exists() is True
        assert Answer.objects.filter(user=self.user, question=questions[1], choice_id=choices[1]).exists() is True
        assert Answer.objects.filter(user=self.user, question=questions[2], choice_id=choices[2]).exists() is True
