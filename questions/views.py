from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView, CreateView
from django.forms.formsets import formset_factory
from django.http import HttpResponse

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

    def form_valid(self, formset):
        # Assuming every query yield the same question_set
        correct_answer_count = 0
        for f, q in zip(formset, self.object.question_set.all()):
            if f.cleaned_data['answer'] ==  q.correct_answer: #  hard-coding 'answer' here; appear in forms.py
                correct_answer_count += 1
        return HttpResponse(f'You have answered {correct_answer_count}/{self.object.question_set.count()} correctly')


class PaperCreateView(CreateView):
    pass
    # Using dynamic formset to create the whole paper instead of questions...