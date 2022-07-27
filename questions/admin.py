from django.contrib import admin

from .models import Paper, Section, Question, UserQuestion

admin.site.register(Paper)
admin.site.register(Section)
admin.site.register(Question)
admin.site.register(UserQuestion)
