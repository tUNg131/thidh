from django.contrib import admin

from questions.forms import QuestionForm
from .models import Paper, Section, Question, UserQuestion


class QuestionAdmin(admin.ModelAdmin):
    form = QuestionForm

admin.site.register(Paper)
admin.site.register(Section)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserQuestion)
