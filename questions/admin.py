from django.contrib import admin

from .models import Question, Paper

admin.site.register(Question)
admin.site.register(Paper)