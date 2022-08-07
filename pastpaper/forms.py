from django import forms

from .models import PaperHistory


class SplitAnswerOptionsField(forms.MultiValueField):
    pass


class DoPaperForm(forms.ModelForm):
    class Meta:
        model = PaperHistory
        fields = ("answer_options",)

    #  answer_options = MultivalueField
    #  method full_check()
    def __init__(self, json_data, **kwargs):
        super().__init__(**kwargs)

        self.json_data = json_data

        # Initialise answer_options field.
        sub_fields = []
        for section in json_data["sections"]:
            for question in section["questions"]:
                option_texts = question["options"]
                choices = zip(range(len(option_texts)), option_texts)
                sub_fields.append(
                    forms.ChoiceField(widget=forms.RadioSelect, choices=choices)
                )
        self.fields.update({
            "answer_options": SplitAnswerOptionsField(sub_fields)
        })

    def get_context(self):
        json_data = self.json_data.copy()
        context = super().get_context()




