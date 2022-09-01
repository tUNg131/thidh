from django.forms import ModelForm
from django.forms.fields import MultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.utils import ErrorList as DjangoErrorList

from .models import PaperHistory


def get_choice_tuples(options):
    return [(str(i), o) for i, o in zip(range(len(options)), options)]


class ErrorList(DjangoErrorList):
    template_name = "pastpapers/forms/errors/list/ul.html"


class QuestionField(MultipleChoiceField):
    widget = CheckboxSelectMultiple

    def __init__(self, *args, correct_option, **kwargs):
        super().__init__(*args, **kwargs)
        self.correct_option = correct_option


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

        for i, (option_texts, correct_option) in enumerate(zip(paper.questions, paper.correct_options)):
            choices = get_choice_tuples(option_texts)
            name = self.field_name_template % i
            fields[name] = self.question_field_class(correct_option=correct_option, choices=choices, required=False)
            if self.instance.answer_options:
                initial[name] = self.instance.answer_options[i]

        self.initial.update(initial)
        self.fields = fields # Remove all other fields

        self.instance.paper = paper
        self.instance.user = user

        action = self.data.get("action", "save")
        self._is_submitting = action == "submit"

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



