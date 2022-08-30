from django.forms import ModelForm


def get_choice_tuples(options):
    return [(str(i), o) for i, o in zip(range(len(options)), options)]


class PaperForm(ModelForm):
    question_field_class = QuestionField

    class Meta:
        model = PaperHistory
        # Exclude all
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
