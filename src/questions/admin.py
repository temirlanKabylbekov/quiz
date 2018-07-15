from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from nested_inline.admin import NestedModelAdmin, NestedStackedInline

from questions.models import Question, QuestionChoice, QuestionList


class CheckOrderIds:

    def __init__(self, instance, related_obj_name, order_ids_str):
        self.instance = instance
        self.related_obj_name = related_obj_name
        self.order_ids_str = order_ids_str

    def get_int_order_ids(self):
        order_ids = self.order_ids_str.split(',')
        try:
            return [int(order_id) for order_id in order_ids]
        except ValueError:
            raise forms.ValidationError(_('Check format of passed data'))

    def check_with_instance_order_ids(self, order_ids):
        actual_ids = list(getattr(self.instance, self.related_obj_name).order_by('id').values_list('id', flat=True))
        if actual_ids != sorted(order_ids):
            raise forms.ValidationError(_('Passed invalid choice id'))
        return order_ids

    @property
    def validated_data(self):
        if not self.order_ids_str:
            return ''
        int_order_ids = self.get_int_order_ids()
        return self.check_with_instance_order_ids(int_order_ids)


class OrderFormMixin:

    def _set_order(self, order_ids):
        raise NotImplemented('implement in subclass')

    def clean_order(self):
        return CheckOrderIds(self.instance, self._related_obj_name, self.cleaned_data['order']).validated_data

    def save(self, commit=True):
        instance = super().save(commit)
        self._set_order(self.cleaned_data['order'])
        return instance


class QuestionForm(OrderFormMixin, forms.ModelForm):

    order = forms.CharField(
        required=False,
        label=_('Choice order in question'),
        help_text=_('List the choice ids separated by a comma without a space'))

    def __init__(self, *args, **kwargs):
        self._related_obj_name = 'choices'
        return super().__init__(*args, **kwargs)

    def _set_order(self, order_ids):
        self.instance.set_questionchoice_order(order_ids)


class QuestionListForm(OrderFormMixin, forms.ModelForm):

    order = forms.CharField(
        required=False,
        label=_('Question order in question list'),
        help_text=_('List the question ids separated by a comma without a space'))

    def __init__(self, *args, **kwargs):
        self._related_obj_name = 'questions'
        return super().__init__(*args, **kwargs)

    def _set_order(self, order_ids):
        self.instance.set_question_order(order_ids)


class QuestionChoiceInline(NestedStackedInline):

    model = QuestionChoice
    exclude = ['modified']
    readonly_fields = ['choice_id']
    extra = 1
    fk_name = 'question'

    def choice_id(self, obj):
        return obj.id
    choice_id.short_description = _('Question choice id')


class QuestionInline(NestedStackedInline):

    model = Question
    readonly_fields = ['pk']
    exclude = ['modified']
    readonly_fields = ['question_id']
    extra = 1
    fk_name = 'question_list'
    inlines = [QuestionChoiceInline]
    form = QuestionForm

    def question_id(self, obj):
        return obj.id
    question_id.short_description = _('Question id')


class QuestionListAdmin(NestedModelAdmin):

    model = QuestionList
    exclude = ['modified']
    inlines = [QuestionInline]
    form = QuestionListForm


admin.site.register(QuestionList, QuestionListAdmin)
