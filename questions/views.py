from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView, CreateView
from django.http import HttpResponse

from .models import Paper
from .forms import PaperForm


class PaperDetailView(SingleObjectMixin, FormView):
    # Need to check the prefetch_related. https://stackoverflow.com/questions/19649370/django-can-you-tell-if-a-related-field-has-been-prefetched-without-fetching-it
    model = Paper
    template_name = 'paper_details.html'
    form_class = PaperForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.object:
            kwargs.update({
                'paper': self.object
            })
        return kwargs

    def form_valid(self, form):
        correct_count = total_count = 0
        for q in self.object.questions.all():
            form_answer = form.cleaned_data.get(f'question-{q.id}', None)
            if form_answer == q.correct_answer:
                correct_count += 1
            total_count += 1
        return HttpResponse(f'You have answered {correct_count}/{total_count} correctly')


class QuestionCreateView(CreateView):
    pass
    # Using dynamic formset to create the whole paper instead of questions...