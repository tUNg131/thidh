from django.views.generic.detail import DetailView
from django.forms.formsets import formset_factory

from .models import Paper
from .forms import QuestionForm, BaseQuestionFormSet


class PaperDetailView(DetailView):
    model = Paper
    template_name = 'paper_details.html'

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            questions_data = []
            questions = self.object.question_set

            for q in questions.all():
                question_text = q.question_json['question_text']
                answers = q.question_json['answers']
                choices = [
                    (1, answers[0]),  # many hard coding here
                    (2, answers[1]),
                    (3, answers[2]),
                    (4, answers[3]),
                ]
                questions_data.append((question_text, choices))

            question_form_set_class_name = formset_factory(
                QuestionForm, formset=BaseQuestionFormSet, extra=questions.count())
            context['formset'] = question_form_set_class_name(questions_data)
        context.update(kwargs)
        return super().get_context_data(**context)
