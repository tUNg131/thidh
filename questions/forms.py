from django import forms
from django.utils.translation import gettext as _

from .models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"


class AnswerField(forms.ChoiceField):
    BLANK_OPTION = "---"

    def __init__(self, *, correct_choice, **kwargs):
        choices = kwargs.pop("choices")

        correct_choice_in_choices = False
        for c, _ in choices:
            if c == "n":
                raise ValueError("Choice key can't be 'n'.")
            if correct_choice == c:
                correct_choice_in_choices = True
        if not correct_choice_in_choices:
            raise ValueError("Invalid correct choice.")

        choices = [("n", AnswerField.BLANK_OPTION)] + choices
        super().__init__(choices=choices, **kwargs)

        self.correct_choice = correct_choice

    def is_correct(self, value):
        return self.correct_choice == value


class PaperForm(forms.Form):
    field_name_template = "question-{}"

    def __init__(self, paper, **kwargs):
        super().__init__(**kwargs)

        fields = {}
        for s in paper.sections.distinct():
            for q in s.questions.all():
                field_name = PaperForm.field_name_template.format(q.id)
                correct_choice = "n"
                choices = []
                for i, c in enumerate(q.choices.all()):
                    i = str(i)
                    choices.append((i, c.text))
                    if c.is_correct:
                        correct_choice = i
                fields[field_name] = AnswerField(
                    choices=choices, correct_choice=correct_choice, label="Answer")

        self.paper = paper
        self.fields.update(fields)

    def get_context(self):
        sections = []
        hidden_fields = []
        top_errors = self.non_field_errors().copy()

        for s in self.paper.sections.distinct():
            questions = []
            for q in s.questions.all():
                name = PaperForm.field_name_template.format(q.id)
                bf = self[name]
                bf_errors = self.error_class(bf.errors, renderer=self.renderer)
                if bf.is_hidden:
                    if bf_errors:
                        top_errors += [
                            _("(Hidden field %(name)s) %(error)s")
                            % {"name": name, "error": str(e)}
                            for e in bf_errors
                        ]
                    hidden_fields.append(bf)
                else:
                    errors_str = str(bf_errors)
                    question_text = q.text
                    questions.append({
                        "text": question_text,
                        "field": (bf, errors_str),
                    })
            instructions = s.text
            sections.append({
                "instruction": instructions,
                "questions": questions,
            })
