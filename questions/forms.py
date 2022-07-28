from django import forms
from django.core.exceptions import ValidationError
from .models import Question, get_choices
from django.utils.translation import gettext as _


def get_index_iter():
    def index_iter():
        num = 0
        while True:
            yield num
            num += 1
    return index_iter()


class QuestionJSONWidget(forms.MultiWidget):
    def __init__(self, choices, attrs=None):
        widgets = [forms.Textarea(attrs=attrs)]
        for choice in choices:
            widgets.append(forms.TextInput(attrs=attrs))
        super().__init__(widgets)
        self.choices = choices

    def decompress(self, value):
        if value:
            question_text = value["qnt"]
            choices = value["chs"]
            return [question_text, *choices]
        return [None]*(len(self.choices)+1)


class HiddenQuestionJSONWidget(QuestionJSONWidget):
    def __init__(self, choices, attrs=None):
        super().__init__(choices, attrs)
        for widget in self.widgets:
            widget.input_type = 'hidden'


class QuestionJSONDataField(forms.MultiValueField):
    error_messages_template = "Enter a valid answer {}."

    def __init__(self, choices, **kwargs):
        errors = self.default_error_messages.copy()
        if "error_messages" in kwargs:
            errors.update(kwargs["error_messages"])
        localize = kwargs.get("localize", False)
        fields = [
            forms.CharField(
                error_messages={"invalid": "Enter a valid question text."},
                localize=localize
            )
        ]
        for choice in choices:
            if not isinstance(choice, str):
                choice = str(choice)
            error_message = QuestionJSONDataField.error_messages_template.format(choice)
            
            fields.append(
                forms.CharField(
                    error_messages={"invalid": error_message},
                    localize=localize
                )
            )

        self.widget = QuestionJSONWidget(choices)
        self.hidden_widget = HiddenQuestionJSONWidget(choices)

        super().__init__(fields, **kwargs)
        self.choices = choices
        

    def compress(self, data_list):
        if data_list:
            choices = self.choices
            for data, choice in zip(data_list, choices):
                if data in self.empty_values:
                    error_message = QuestionJSONDataField.error_messages_template.format(
                        choice)
                    raise ValidationError(
                        error_message, code=f"invalid_{choice}"
                    )
            question_text, *choices = data
            result = {
                "qnt": question_text,
                "chs": choices
            }
            return result
        return None


class QuestionForm(forms.ModelForm):
    json_data = QuestionJSONDataField(['A', 'B', 'C', 'D'])
    class Meta:
        model = Question
        fields = '__all__'


class PaperForm(forms.Form):
    template_name = "paper_form_snippet.html"

    def __init__(self, paper=None, **kwargs):
        if paper is None:
            raise ValueError("Paper is missing")

        self.paper = paper

        sections = []
        fields = {}

        for s in paper.sections.all():
            questions = []
            for q in s.questions.all():
                field_name = f"question-{q.id}"
                choices = get_choices(q.json_data["chs"])
                fields[field_name] = forms.ChoiceField(choices=choices)

                question_text = q.json_data["qnt"]
                questions.append({
                    "text": question_text,
                    "field_name": field_name,
                })

            instructions = s.instruction_text
            sections.append({
                "instructions": instructions,
                "questions": questions
            })
        
        self.sections = sections

        super().__init__(**kwargs)

        self.fields.update(fields)

    def get_context(self):
        sections = []
        hidden_fields = []
        top_errors = self.non_field_errors().copy()

        for section in self.sections:
            questions = []
            for question in section["questions"]:
                name = question["field_name"]
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
                    question_text = question["text"]
                    questions.append({
                        "text": question_text,
                        "field": (bf, errors_str),
                    })
            instructions = section["instructions"]
            sections.append({
                "instructions": instructions,
                "questions": questions,
            })

        return {
            "sections": sections,
            "hidden_fields": hidden_fields,
            "errors": top_errors,
        }
