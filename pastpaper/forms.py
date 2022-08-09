from django.forms import Form
from django.forms.fields import ChoiceField
from django.forms.widgets import RadioSelect
from django.forms.utils import ErrorDict
from django.utils.safestring import mark_safe

from .choices import get_choice_tuples
from .models import PastPaper


class WrongAnswerDict(ErrorDict):
    pass


class AnswerField(ChoiceField):
    widget = RadioSelect

    def __init__(self, *, correct_choice, **kwargs):
        super().__init__(**kwargs)
        self.correct_choice = correct_choice

    def is_correct(self, value):
        return value == self.correct_choice


class DoPaperForm(Form):
    template_name = "do_paper_form_snippet.html"

    def __init__(self, paper, **kwargs):
        super().__init__(**kwargs)

        if not isinstance(paper, PastPaper):
            raise ValueError("Has to be instance of PastPaper")
        self._paper = paper

        self._wrong_answers = None

        fields = {}
        questions = self.get_questions(paper.json_data)
        for i, (q, correct_option) in enumerate(zip(questions, paper.correct_options)):
            choices = get_choice_tuples(options=q["options"])
            field_name = self.get_field_name(i)
            fields[field_name] = AnswerField(correct_option, choices=choices)

        self.fields = fields

    def get_questions(self, json_data):
        for s in json_data["sections"]:
            for q in s["questions"]:
                yield q

    @property
    def wrong_answers(self):
        if self._wrong_answers is None:
            self.check_answers()
        return self._wrong_answers

    def get_context(self):
        context = super().get_context()
        fields = context["fields"]
        paper_json = self._paper.json_data

        for i, q in enumerate(self.get_questions(paper_json)):
            bf, error_str = fields[i]
            name = self.get_field_name(i)
            wrong_answer_str = self.wrong_answers.get(name, "")
            wrong_answer_str = mark_safe(wrong_answer_str)
            q.update({
                "field_error": error_str,
                "field": bf,
                "wrong_answer": wrong_answer_str,
            })
        context.update({"paper": paper_json})
        return context
                
    def check_answers(self):
        self._wrong_answers = WrongAnswerDict()
        if not hasattr(self, "cleaned_data"):
            return

        for name, value in self.cleaned_data.items():
            field = self.fields[name]
            if not field.is_correct(value):
                self._wrong_answers[name] = "Wrong!"

    def get_field_name(i):
        return f"question-{i}"








