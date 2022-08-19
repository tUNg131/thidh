from django.contrib import admin

from . import models

admin.site.register(models.PastPaper)
admin.site.register(models.PaperHistory)
