from django.views.generic.detail import DetailView
from .models import Question

import json


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'question_detail.html'

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            question_body, answers = json.load(self.object.question_json)
            context['question_body'] = question_body
            context['answers'] = answers
        context.update(kwargs)
        return super().get_context_data(**context)
