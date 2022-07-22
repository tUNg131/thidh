from django.urls import path

from . import views

app_name = 'questions'
urlpatterns = [
    path('<int:pk>/', views.PaperDetailView.as_view()),
    # path('<int:question_id>/', views.QuestionDetailView.as_view(), name='details'),
    # path('<int:question_id>/solution', views.solution, name='solution'),
]