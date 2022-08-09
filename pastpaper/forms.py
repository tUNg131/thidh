from django.forms import ModelForm
from django.forms.fields import ChoiceField
from django.forms.widgets import RadioSelect
from django.forms.utils import ErrorDict


class WrongAnswerDict(ErrorDict):
    pass


class AnswerField(ChoiceField):
    widget = RadioSelect

    def __init__(self, *, correct_choice, **kwargs):
        super().__init__(**kwargs)
        self.correct_choice = correct_choice


class DoPaperForm(ModelForm):
    def __init__(self, json_data, **kwargs):
        super().__init__(**kwargs)

        self.json_data = json_data
        self._wrong_answers = None

        fields = {}
        index = 0
        for section in json_data["sections"]:
            for question in section["questions"]:
                option_texts = question["options"]
                # choices are not correct anymore
                choices = list(zip(range(len(option_texts)), option_texts))
                field_name = f"question-{index}"
                fields[field_name] = AnswerField(choices=choices)
                index += 1
        self.fields = fields

    @property
    def wrong_answers(self):
        if self._wrong_answers is None:
            self.check_answers()
        return self._wrong_answers

    def get_context(self):
        context = super().get_context()

    def check_answers(self):
        self._wrong_answers = WrongAnswerDict()
        if not hasattr(self, "cleaned_data"):
            return

        for name, value in self.cleaned_data.items():
            field = self.fields[name]








