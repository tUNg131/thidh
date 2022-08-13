from django.urls import path

from . import views

app_name = "pastpaper"
urlpatterns = [
    path("<int:pk>/", views.DoPaperView.as_view()),
    path('test/', views.TestView.as_view())
]