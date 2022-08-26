from django.forms import ModelForm, Form
from django.forms.utils import RenderableMixin
from django.forms.renderers import get_default_renderer
from django.forms.boundfield import BoundField
from django.forms.fields import MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.utils.safestring import mark_safe

from .models import PaperHistory, get_questions_from_json
from .choices import get_choice_tuples, MODEL_BLANK_CHAR

class TestForm(Form):
    template_name = "pastpapers/forms/test.html"
    OPTIONS = [
        ("a", "A"),
        ("b", "B"),
        ("c", "C"),
        ("d", "D"),
    ]
    field1 = MultipleChoiceField(widget=CheckboxSelectMultiple, choices=OPTIONS)


class QuestionBoundField(BoundField):
    @property
    def result(self):
        return self.form.results.get(self.name, None)


class QuestionField(MultipleChoiceField):
    widget = CheckboxSelectMultiple

    def __init__(self, *, correct_option, **kwargs):
        super().__init__(**kwargs)
        self.correct_option = correct_option
    
    def check_answer(self, value):
        breakpoint()
        return len(value) == 1 and self.correct_option in value

    def get_bound_field(self, form, field_name):
        return QuestionBoundField(form, self, field_name)


class PaperForm(ModelForm):
    question_field_class = QuestionField
    field_name_template = "question-%s"

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

        self.template_name = paper.template_name

        for i, (option_texts, correct_option) in enumerate(zip(paper.questions, paper.correct_options)):
            choices = get_choice_tuples(option_texts)
            name = self.field_name_template % i
            fields[name] = self.question_field_class(
                correct_option=correct_option, choices=choices, required=False)
            if self.instance.answer_options:
                initial[name] = self.instance.answer_options[i]

        self.initial.update(initial)
        self.fields = fields # Remove all other fields

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
        fields = context.pop("fields")
        questions = []
        question_errors = []
        for bf, error_str in fields:
            questions.append(bf)
            question_errors.append(error_str)
        context.update({
            "questions": questions,
            "question_errors": question_errors
        })
        return context

    def _post_clean(self):
        # super()._post_clean()

        # answer_options = []
        # for name in self.fields:
        #     field = self.fields[name]
        #     if not isinstance(field, self.question_field_class):
        #         continue

        #     value = self.cleaned_data.get(name)
        #     if name in self._errors or value in field.empty_values:
        #         answer_options.append(MODEL_BLANK_CHAR)
        #     else:
        #         answer_options.append(value)
        # self.instance.answer_options = answer_options

        # if self.is_submitting:
        #     self.check_answers()

        # Validate the model here (question_count == answer_count)
        pass

    def check_answers(self):
        # self._results = {}
        # if not hasattr(self, "cleaned_data"):
        #     return

        # correct_option_count = 0
        # for name, value in self.cleaned_data.items():
        #     field = self.fields[name]
        #     if not isinstance(field, self.question_field_class):
        #         continue

        #     is_correct = field.check_answer(value)
        #     # get correct option here
        #     self._results[name] = self.question_result_class(
        #         is_correct=is_correct, renderer=self.renderer
        #     )
        #     if is_correct:
        #         correct_option_count += 1
        # self.instance.correct_option_count = correct_option_count
        pass

