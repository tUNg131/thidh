from django.db import models
from thidh.accounts.models import User


class PastPaper(models.Model):
    # Validation: correct format..
    template_name = models.CharField(max_length=50)
    questions = models.JSONField() # List of list of option text
    correct_options = models.JSONField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class PaperHistory(models.Model):
    # TODO: validation
    answer_options = models.JSONField()
    # Check only one History has the correct option count..
    correct_option_count = models.SmallIntegerField(blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    paper = models.ForeignKey(PastPaper, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
