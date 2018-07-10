from django.db import models

from app.models import TimestampedModel


class Answer(TimestampedModel):

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, null=True)
    choice = models.ForeignKey('questions.QuestionChoice', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.question}:{self.user}'

    class Meta:
        unique_together = ('user', 'question')
