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
    template_name = 'question_form_snippet.html'

    def __init__(self, question_text="", choices=None, **kwargs):
        if choices is None:
            choices = []
        self.question_text = question_text

        super().__init__(**kwargs)

        self.fields['answer'] = forms.ChoiceField(choices=choices, label="Answer:")


class BaseQuestionFormSet(forms.BaseFormSet):
    def __init__(self, form_kwargs_list=None, **kwargs):
        self.form_kwargs_list = form_kwargs_list or []

        super().__init__(**kwargs)

    def get_form_kwargs(self, index):
        return self.form_kwargs_list[index]

class SectionForm(forms.Form):
    template_name = 'section_snippet.html'
    
    def __init(self, form_context_data=None, **kwargs):
        super().__init__(**kwargs)

        form_context_data = form_context_data or {}

        fields = {}
        for id, question in form_context.items():
            question_text = question['qst']
            choices = get_choices(question['ans'])
            fields[f'question-{id}'] = forms.ChoiceField(choices)
            

class PaperForm(forms.Form):
    template_name = 'paper_form_snippet.html'

    def __init__(self, paper, **kwargs):
        self.paper = paper

        sections = []
        fields = {}
        question_index = get_index_iter()

        for s in paper.sections:
            questions = []
            for q in s.questions:
                field_name = f"question-{next(question_index)}"
                self.fields[field_name] = forms.ChoiceField(choices=get_choices(q.json_data['chs']))

                questions.append({
                    "question_text": q.json_data['qnt'],
                    "field_name": field_name
                })

            sections.append({
                "section_instruction": s['instr'],
                "questions": questions
            })
        
        self.form_structure = sections
        
        super().__init__(**kwargs)

        self.fields.update(fields)

    def get_context(self):
        sections = []
        hidden_fields = []
        top_errors = self.non_field_errors().copy()

        for section in self.form_structure:
            questions = []
            for question in section["questions"]:
                name = question.pop("field_name")
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
                    # RemovedInDjango50Warning.
                    questions.append({
                        "question_text": question["question_text"],
                        "choice_field": (bf, errors_str)
                    })
            


        for name, bf in self._bound_items():
            
        return {
            "form": self,
            "fields": fields,
            "hidden_fields": hidden_fields,
            "errors": top_errors,
        }

# [section1, {"instruction": "", "questions": [question1, {qst:"", ans:[ans1, ""]}]}]

# {% for section in sections %}
#   {{ section instruction }}
#   {% for question in questions %}
#       {{ question_text }}
#       {{ field }}