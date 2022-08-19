from django.urls import path

from . import views

app_name = "pastpapers"
urlpatterns = [
    path("<int:pk>/", views.DoPaperView.as_view()),
    path('test/', views.TestView.as_view(), name='test_index'),
    path('form/', views.TestFormView.as_view()),
]