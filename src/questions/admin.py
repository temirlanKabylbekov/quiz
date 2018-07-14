from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline

from questions.models import Question, QuestionChoice, QuestionList


class QuestionChoiceInline(NestedStackedInline):
    model = QuestionChoice
    exclude = ['modified']
    extra = 1
    fk_name = 'question'


class QuestionInline(NestedStackedInline):
    model = Question
    exclude = ['modified']
    extra = 1
    fk_name = 'question_list'
    inlines = [QuestionChoiceInline]


class QuestionListAdmin(NestedModelAdmin):
    model = QuestionList
    exclude = ['modified']
    inlines = [QuestionInline]


admin.site.register(QuestionList, QuestionListAdmin)
