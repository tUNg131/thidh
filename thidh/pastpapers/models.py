from django.contrib.postgres.fields import ArrayField
from django.db import models

from .choices import get_choice_tuples, get_choice_tuples_with_blank
from thidh.accounts.models import User

DEFAULT_CHOICES = get_choice_tuples()
DEFAULT_CHOICES_WITH_BLANK = get_choice_tuples_with_blank()


def get_questions_from_json(json_data):
    for s in json_data["sections"]:
        for q in s["questions"]:
            yield q


class PastPaper(models.Model):
    # Validation: correct format..
    template_name = models.CharField(max_length=30)
    questions = models.JSONField()
    correct_options = models.JSONField()
    created_time = models.TimeField(auto_now_add=True)
    updated_time = models.TimeField(auto_now=True)


class PaperHistory(models.Model):
    # TODO: validation
    answer_options = models.JSONField()
    # Check only one History has the correct option count..
    correct_option_count = models.SmallIntegerField(blank=True, null=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_time = models.TimeField(auto_now=True)

    paper = models.ForeignKey(PastPaper, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
