from django.urls import path

from . import views

app_name = "pastpapers"
urlpatterns = [
    path("<int:pk>/", views.DoPaperView.as_view()),
]