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
    template_name = "paper_form_snippet.html"
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

        self.wrong_answers = None
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
                    wrong_answer_str = ""
                    if self.wrong_answers:
                        # Very cumbersome. Need to rewrite this. Have a system like error.
                        wrong_answer_str = str(self.wrong_answers.get(name, ""))
                    questions.append({
                        "text": question_text,
                        "field": (bf, errors_str, wrong_answer_str),
                    })
            instructions = s.instructions
            sections.append({
                "instructions": instructions,
                "questions": questions,
            })
        return {
            "sections": sections,
            "hidden_fields": hidden_fields,
            "errors": top_errors,
        }

    def full_check(self):
        if not hasattr(self, "cleaned_data"):
            self.full_clean()

        self.wrong_answers = {}
        for name, value in self.cleaned_data.items():
            field = self.fields[name]
            if not isinstance(field, AnswerField):
                continue
            if not field.is_correct(value):
                self.wrong_answers[name] = "Wrong answer!"


