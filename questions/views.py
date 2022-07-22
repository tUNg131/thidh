from django.views.generic.detail import SingleObjectMixin
from django.views.generic import FormView
from django.forms.formsets import formset_factory

from .models import Paper, question_to_dict
from .forms import QuestionForm, BaseQuestionFormSet


class PaperDetailView(SingleObjectMixin, FormView):
    model = Paper
    template_name = 'paper_details.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_class(self):
        if self.object:
            return formset_factory(
                QuestionForm,
                formset=BaseQuestionFormSet,
                extra=self.object.question_set.count()
            )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.object:
            form_kwargs_list = [question_to_dict(q) for q in self.object.question_set.all()]
            kwargs.update({
                'form_kwargs_list': form_kwargs_list
            })
        return kwargs
