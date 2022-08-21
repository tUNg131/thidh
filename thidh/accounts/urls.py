from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("password_change/", views.PasswordChangeView.as_view()),
    path("password_change/done/", views.PasswordChangeDoneView.as_view()),
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", views.PasswordResetDoneView.as_view()),
    path("reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view()),
    path("reset/done/", views.PasswordResetCompleteView.as_view()),
]