import itertools

from django.forms import ModelForm, Form
from django.forms.utils import RenderableMixin
from django.forms.renderers import get_default_renderer
from django.forms.boundfield import BoundField
from django.forms.fields import ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.utils.safestring import mark_safe

from .models import PaperHistory, get_questions_from_json
from .choices import get_choice_tuples, MODEL_BLANK_CHAR

class QuestionWidget(CheckboxSelectMultiple):
    option_template_name = "pastpapers/checkbox_option.html"
    template_name = "pastpapers/question.html"
    def optgroups(self, name, value, attrs=None):
        groups = super().optgroups(name, value, attrs)
        return groups

class TestForm(Form):
    template_name = "pastpapers/forms/test.html"
    OPTIONS = [
        ("a", "A"),
        ("b", "B"),
        ("c", "C"),
        ("d", "D"),
    ]
    field1 = MultipleChoiceField(widget=QuestionWidget, choices=OPTIONS)


class QuestionResult(RenderableMixin):
    template_name = "pastpapers/forms/question-result.html"

    def __init__(self, *args, is_correct=None, renderer=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_correct = is_correct
        self.renderer = renderer or get_default_renderer()
        # Need to tell the correct answers as well...

    def get_context(self):
        if self.is_correct is None:
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


class PaperForm(ModelForm):
    question_field_class = QuestionField
    question_result_class = QuestionResult
    field_name_template = "question-%s"
    template_name = "pastpapers/forms/paper-form.html"

    class Meta:
        model = PaperHistory
        exclude = (
            "answer_options",
            "correct_option_count",
            "paper",
            "user",
        )

    def __init__(self, paper=None, user=None, **kwargs):
        self._results = None

        form_opts = self._meta
        model_opts = form_opts.model._meta

        paper_class = model_opts.get_field('paper').remote_field.model
        if not isinstance(paper, paper_class):
            raise ValueError(f"Paper has to be instance of {paper_class}")

        user_class = model_opts.get_field('user').remote_field.model
        if not isinstance(user, user_class):
            raise ValueError(f"User has to be instance of {user_class}")

        super().__init__(**kwargs)

        fields = {}
        initial = {}

        paper_json = paper.json_data
        questions_iter = get_questions_from_json(paper_json)
        correct_options = paper.correct_options
        answer_options = self.instance.answer_options or []
        for i, (q, correct_option, answer_option) in \
                enumerate(itertools.zip_longest(questions_iter, correct_options, answer_options)):
            option_texts = q["options"]
            choices = get_choice_tuples(option_texts)
            name = self.field_name_template % i
            fields[name] = self.question_field_class(
                correct_option=correct_option, choices=choices, required=False)
            if answer_option is None:
                continue
            initial[name] = answer_option

        self.initial.update(initial)
        self.fields.update(fields)

        self.instance.paper = paper
        self.instance.user = user

        action = self.data.get("action", "save")
        self._is_submitting = action == "submit"

    @property
    def results(self):
        if self._results is None:
            self.check_answers()
        return self._results

    @property
    def is_submitting(self):
        return self._is_submitting

    def get_context(self):
        context = super().get_context()
        fields_iter = iter(context.pop("fields"))

        paper = self.instance.paper
        fields = []
        sections = []
        for s in paper.json_data["sections"]:
            questions = []
            for q in s["questions"]:
                while True:
                    bf, error_str = next(fields_iter)
                    if isinstance(bf.field, self.question_field_class):
                        question_text = q["text"]
                        question_text = mark_safe(question_text)
                        result_str = str(bf.result)
                        result_str = mark_safe(result_str)
                        questions.append((bf, error_str, question_text, result_str))
                        break
                    else:
                        fields.append((bf, error_str))
            sections.append({
                "instructions": s["instructions"],
                "questions": questions
            })
        paper = {
            "instructions": paper.json_data["instructions"],
            "sections": sections
        }
        context.update({
            "paper": paper,
            "fields": fields
        })
        return context

    def _post_clean(self):
        super()._post_clean()

        answer_options = []
        for name in self.fields:
            field = self.fields[name]
            if not isinstance(field, self.question_field_class):
                continue

            value = self.cleaned_data.get(name)
            if name in self._errors or value in field.empty_values:
                answer_options.append(MODEL_BLANK_CHAR)
            else:
                answer_options.append(value)
        self.instance.answer_options = answer_options

        if self.is_submitting:
            self.check_answers()

        # Validate the model here (question_count == answer_count)

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
            # get correct option here
            self._results[name] = self.question_result_class(
                is_correct=is_correct, renderer=self.renderer
            )
            if is_correct:
                correct_option_count += 1
        self.instance.correct_option_count = correct_option_count
