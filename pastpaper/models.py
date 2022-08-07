from django.contrib.postgres.fields import ArrayField
from django.db import models
from accounts.models import User
from .choices import OPTIONS


class PastPaper(models.Model):
    # Validation: correct format..
    json_data = models.JSONField(verbose_name="JSON Data")
    # {
    #     "instructions": "",
    #     "sections": [{
    #         "instructions": "",
    #         "questions": [{
    #             "text": "",
    #             "options": ["", "", ..],
    #         }]
    #     }]
    # }
    correct_options = ArrayField(
        models.CharField(max_length=1, choices=OPTIONS)
    )
    created_time = models.TimeField(auto_now_add=True)
    updated_time = models.TimeField(auto_now=True)


class PaperHistory(models.Model):
    # Validation: valid option...
    answer_options = ArrayField(
        models.CharField(max_length=1, choices=OPTIONS)
    )
    # Validation: can't > number of questions...
    correct_option_count = models.SmallIntegerField()
    blank_option_count = models.SmallIntegerField()
    is_active = models.BooleanField()
    created_time = models.TimeField(auto_now_add=True)
    updated_time = models.TimeField(auto_now=True)

    paper = models.ForeignKey(PastPaper, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
