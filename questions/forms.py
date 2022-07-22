from django import forms


class QuestionForm(forms.Form):
    template_name = 'question_form_snippet.html'

    def __init__(self, question_text="", choices=None, **kwargs):
        if choices is None:
            choices = []
        self.question_text = question_text

        super().__init__(**kwargs)

        self.fields['answer'] = forms.ChoiceField(choices=choices, label="Answer:")


class BaseQuestionFormSet(forms.BaseFormSet):
    def __init__(self, questions_data=None, **kwargs):
        self.questions_data = questions_data or []

        super().__init__(**kwargs)

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)

        question_text, choices = self.questions_data[index]
        kwargs.update({
            'question_text': question_text,
            'choices': choices
        })
        return kwargs
