from app.test import mixer


class Factory:

    @classmethod
    def question_list(cls, num_questions, num_choices):
        quest_list = mixer.blend('questions.QuestionList')
        [cls.question(num_choices, question_list=quest_list) for _ in range(num_questions)]
        quest_list.refresh_from_db()
        return quest_list

    @classmethod
    def question(cls, num_choices, **kwargs):
        quest = mixer.blend('questions.Question', **kwargs)
        mixer.cycle(num_choices).blend('questions.QuestionChoice', question=quest)
        quest.refresh_from_db()
        return quest

    @classmethod
    def answered_question_list(cls, question_list, user):
        for question in question_list.questions.iterator():
            random_choice = question.choices.order_by('?').first()
            mixer.blend('answers.Answer', question=question, choice=random_choice, user=user)
        question_list.refresh_from_db()
        return question_list

    @classmethod
    def answered_question_choice(cls, choice, num_answers):
        mixer.cycle(num_answers).blend('answers.Answer', question=choice.question, choice=choice)
        choice.refresh_from_db()
        return choice
