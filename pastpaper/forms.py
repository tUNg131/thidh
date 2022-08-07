from django import forms

from .models import PaperHistory


class DoPaperForm(forms.ModelForm):
    class Meta:
        model = PaperHistory
        fields = ('answer_options',)

    #  answer_options = MultivalueField
    #  method full_check()
    answer_options =




