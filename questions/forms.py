from django import forms
from .models import get_choices
from django.utils.translation import gettext as _


def get_index_iter():
    def index_iter():
        num = 0
        while True:
            yield num
            num += 1
    return index_iter()


class QuestionForm(forms.Form):
    # Need to make these dynamic & modelform
    question_text = forms.CharField(widget=forms.Textarea)
    answer_A = forms.CharField()
    answer_B = forms.CharField()
    answer_C = forms.CharField()
    answer_D = forms.CharField()
    correct_answer = forms.ChoiceField(choices=get_choices())


class PaperForm(forms.Form):
    template_name = 'paper_form_snippet.html'

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
                choices = get_choices(q.json_data['chs'])
                fields[field_name] = forms.ChoiceField(choices=choices)

                question_text = q.json_data['qnt']
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
