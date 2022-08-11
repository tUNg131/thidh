from django.forms import Form
from django.forms.fields import ChoiceField, MultiValueField
from django.forms.widgets import RadioSelect, MultiWidget
from django.forms.utils import ErrorDict
from django.utils.safestring import mark_safe

from .choices import get_choice_tuples
from .models import PastPaper


class PaperWidget(MultiWidget):
    def __init__(self, json_data, widgets, **kwargs):
        self._json_data = json_data # Deep copy this?

    def decompress(self, value):
        if value:
            return value
        return None

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        for w in context['widget']['subwidgets']:




class AnswerField(ChoiceField):
    widget = RadioSelect

    def __init__(self, *, correct_choice, **kwargs):
        super().__init__(**kwargs)
        self.correct_choice = correct_choice

    def is_correct(self, value):
        return value == self.correct_choice


class PaperField(MultiValueField):
    widget = PaperWidget
    sub_widget = RadioSelect

    def __init__(self, paper, widget=None, **kwargs):
        if not isinstance(paper, PastPaper):
            raise ValueError("Has to be instance of PastPaper")
        self._paper = paper

        fields = []
        sub_widgets = []
        for q in self.get_questions():
            fields.append(
                ChoiceField()
            )
            choices = get_choice_tuples(options=q["options"])
            sub_widgets.append(
                self.sub_widget(choices=choices)
            )

        widget = widget or self.widget
        if isinstance(widget, type):
            widget = widget(sub_widgets)

        super().__init__(fields, widget=widget, **kwargs)

    def get_questions(self):
        for s in self._paper.json_data["sections"]:
            for q in s["questions"]:
                yield q

    def compress(self, data_list):
        if data_list:
            return data_list
        return None


class DoPaperForm(Form):
    template_name = "do_paper_form_snippet.html"

    def __init__(self, paper, record=None, **kwargs):
        if record is None:
            # Construct new instance here
            self.record = model()
            record_data = {}
        else:
            self.record = record
            record_data = record_to_dict(record)

        initial = kwargs.pop("initial", None)
        if initial is not None:
            record_data.update(initial)

        super().__init__(initial=record_data, **kwargs)

        if not isinstance(paper, PastPaper):
            raise ValueError("Has to be instance of PastPaper")
        self._paper = paper

        self._wrong_answers = None

        fields = {}
        questions = self.get_questions()
        for i, (q, correct_option) in enumerate(zip(questions, paper.correct_options)):
            choices = get_choice_tuples(options=q["options"])
            field_name = self.get_field_name(i)
            fields[field_name] = AnswerField(correct_choice=correct_option, choices=choices)

        self.fields = fields

    def get_questions(self):
        for s in self._paper.json_data["sections"]:
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

        for i, q in enumerate(self.get_questions()):
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

    def compress(self):
        # Populate answer options...
        pass

    def check_answers(self):
        self._wrong_answers = [] # make this a list
        if not hasattr(self, "cleaned_data"):
            return

        for name, value in self.cleaned_data.items():
            field = self.fields[name]
            if correct
            if not correct
            if blank

        construct instance here

    @staticmethod
    def get_field_name(i):
        return f"question-{i}"

    def _post_clean(self):
        self.check_answers()










