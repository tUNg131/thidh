from django.contrib import admin

from . import models

admin.site.register(models.Section)
admin.site.register(models.Paper)
admin.site.register(models.PastPaper)
admin.site.register(models.QuestionType)
admin.site.register(models.Question)
admin.site.register(models.Choice)
