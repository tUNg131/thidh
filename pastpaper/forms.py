from django.forms import Form
from django.forms.utils import RenderableMixin
from django.forms.renderers import get_default_renderer
from django.forms.boundfield import BoundField
from django.forms.fields import ChoiceField
from django.forms.widgets import RadioSelect
from django.utils.safestring import mark_safe

from .models import PaperHistory, PastPaper, record_to_dict,
    get_questions_from_json
from .choices import get_choice_tuples, MODEL_BLANK_CHAR


class QuestionResult(RenderableMixin):
    template_name = "questionresult.html"

    def __init__(self, *args, is_correct=None, renderer=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_correct = is_correct
        self.renderer = renderer or get_default_renderer()
        # Need to tell the correct answers as well...

    def get_context(self):
        if is_correct is None:
            result = None
        else:
            result = self
        return {
            "result": result
        }

class QuestionBoundField(BoundField):
    @property
    def result(self):
        return self.form.results.get(
            self.name, self.form.question_result_class(renderer=self.form.renderer)
        )

class QuestionField(ChoiceField):
    widget = RadioSelect

    def __init__(self, *, correct_option, **kwargs):
        super().__init__(**kwargs)
        self.correct_option = correct_option
    
    def check_answer(self, value):
        return value == self.correct_option

    def get_bound_field(self, form, field_name):
        return QuestionBoundField(form, self, field_name)

class PaperForm(Form):
    question_field_class = QuestionField
    question_result_class = QuestionResult
    record_model = PaperHistory
    paper_model = PastPaper
    field_name_template = "question-%s"

    def __init__(self, paper, record=None, **kwargs):
        if not isinstance(paper, self.paper_model):
            raise ValueError("Has to be instance of PastPaper")
        self._paper = paper

        if record is None:
            self.record = self.record_model()
            record_data = {}
        else:
            self.record = record
            record_data = record_to_dict(record)

        initial = kwargs.pop("initial", None)
        if initial is not None:
            record_data.update(initial)
        super().__init__(initial=record_data, **kwargs)

        self._results = None

        fields = {}
        correct_options = paper.correct_options
        iterquestions = get_questions_from_json(paper.json_data)
        for i, (q, correct_option) in enumerate(zip(iterquestions, correct_options)):
            option_texts = q["options"]
            choices = get_choice_tuples(option_texts)
            name = self.field_name_template % i
            fields[name] = self.question_field_class(
                correct_option=correct_option, choices=choices, required=False)

        self.fields.update(fields)

    @property
    def paper(self):
        return self._paper

    @property
    def results(self):
        if self._results is None:
            self.check_answers()
        return self._results

    def get_context(self):
        context = super().get_context()
        iterfields = iter(context.pop("fields"))

        paper_json = self.paper.json_data
        fields = []
        sections = []
        for s in paper_json["sections"]:
            questions = []
            for q in s["questions"]:
                while:
                    bf, error_str = next(iterfields)
                    if isinstance(bf.field, self.question_field_class):
                        result_str = str(bf.result)
                        result_str = mark_safe(result_str)
                        questions.append((bf, error_str, result_str))
                        break
                    else:
                        fields.append((bf, error_str))
            sections.append({
                "instructions": s["instructions"],
                "questions": questions
            })
        paper = {
            "instructions": paper_json["instructions"],
            "sections": sections
        }
        context.update({
            "paper": paper,
            "fields": fields
        })
        return context

    def check_answers(self):
        self._results = {}
        if not hasattr(self, "cleaned_data"):
            return

        correct_option_count = 0
        for name, value in self.cleaned_data.items():
            field = self.fields[name]
            if not isinstance(field, self.question_field_class):
                continue

            is_correct = field.check_answer(value)
            self._results[name] = self.question_result_class(
                is_correct=is_correct, renderer=self.renderer
            )
            correct_option_count += 1
        self.record.correct_option_count = correct_option_count


    def _post_clean(self):
        answer_options = []
        for name in self.fields:
            field = self.fields[name]
            if not isinstance(field, self.question_field_class):
                continue

            value = self.cleaned_data.get(name)
            if name in self_errors or value in field.empty_values:
                answer_options.append(MODEL_BLANK_CHAR)
            else:
                answer_options.append(value)

        self.record.answer_options = answer_options
        
        # Validate the model here (question_count == answer_count)


