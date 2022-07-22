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
    def __init__(self, form_kwargs_list=None, **kwargs):
        self.form_kwargs_list = form_kwargs_list or []

        super().__init__(**kwargs)

    def get_form_kwargs(self, index):
        return self.form_kwargs_list[index]
