from django.db import models


class PastPaper(models.Model):
    json_data = models.JSONField(verbose_name="JSON Data")
    answer_keys = models.CharField(max_length=40)  # Could use multivalue field.
