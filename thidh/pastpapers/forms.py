from django.forms import ModelForm
from django.forms.boundfield import BoundField
from django.forms.fields import MultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.utils import ErrorList as DjangoErrorList
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import PaperHistory


def get_choice_tuples(options):
    return [(str(i), o) for i, o in zip(range(len(options)), options)]


class ErrorList(DjangoErrorList):
    template_name = "pastpapers/forms/errors/list/ul.html"

def validate_one_choice(value):
    if value:
        if len(value) > 1:
            raise ValidationError(
                _("Can't choose more than 1 option.")
            )

class QuestionBoundField(BoundField):
    @property
    def result(self):
        return self.form.results.get(self.name)


class QuestionField(MultipleChoiceField):
    widget = CheckboxSelectMultiple

    def __init__(self, *args, correct_option, **kwargs):
        super().__init__(*args, **kwargs)
        self.correct_option = correct_option

    def get_bound_field(self, form, field_name):
        return QuestionBoundField(form, self, field_name)


class PaperForm(ModelForm):
    question_field_class = QuestionField
    field_name_template = "question_%s"

    class Meta:
        model = PaperHistory
        # Exclude all
        exclude = (
            "answer_options",
            "correct_option_count",
            "paper",
            "user",
        )
    
    def __init__(self, paper=None, user=None, error_class=ErrorList, **kwargs):
        self._results = None

        form_opts = self._meta
        model_opts = form_opts.model._meta

        paper_class = model_opts.get_field('paper').remote_field.model
        if not isinstance(paper, paper_class):
            raise ValueError(f"Paper has to be instance of {paper_class}")

        user_class = model_opts.get_field('user').remote_field.model
        if not isinstance(user, user_class):
            raise ValueError(f"User has to be instance of {user_class}")

        super().__init__(error_class=error_class, **kwargs)

        fields = {}
        initial = {}

        self.template_name = paper.template_name

        action = self.data.get("action", "save")
        self._is_submitting = action == "submit"

        validators = [validate_one_choice] if self._is_submitting else []

        for i, (option_texts, correct_option) in enumerate(zip(paper.questions, paper.correct_options)):
            choices = get_choice_tuples(option_texts)
            name = self.field_name_template % i
            fields[name] = self.question_field_class(
                correct_option=correct_option, choices=choices, required=False, validators=validators)
            if self.instance.answer_options:
                initial[name] = self.instance.answer_options[i]

        self.initial.update(initial)
        self.fields = fields # Remove all other fields

        self.instance.paper = paper
        self.instance.user = user

    @property
    def results(self):
        if self._results is None:
            self.check_answers()
        return self._results

    @property
    def is_submitting(self):
        return self._is_submitting

    def _post_clean(self):
        super()._post_clean()
        answer_options = []
        for name in self.fields:
            field = self.fields[name]
            value = self.cleaned_data.get(name)
            if name in self._errors or value in field.empty_values:
                answer_options.append(None)
            else:
                answer_options.append(value)
        self.instance.answer_options = answer_options

        if self.is_submitting:
            self.check_answers()

    def check_answers(self):
        self._results = {}
        if not hasattr(self, "cleaned_data"):
            return

        correct_option_count = 0
        for name, value in self.cleaned_data.items():
            field = self.fields[name]
            if not isinstance(field, self.question_field_class):
                continue

            correct_option = field.correct_option
            choices = field.choices
            result = []
            for option, _ in choices:
                if option in value:
                    is_correct = option == correct_option
                    if is_correct:
                        correct_option_count += 1
                    result.append(is_correct)
                    continue
                result.append(None)
            # get correct option here
            self._results[name] = result

        for name, _ in self.errors.items():
            bf = self[name]
            field = self.fields[name]
            value = bf.data
            result = []
            for option, _  in field.choices:
                if option in value:
                    result.append(False)
                    continue
                result.append(None)
            self._results[name] = result

        self.instance.correct_option_count = correct_option_count