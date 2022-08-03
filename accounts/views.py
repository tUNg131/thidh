from django.contrib.auth import views


class LoginView(views.LoginView):
    next_page = "paper-list"
    template_name = "login.html"


class LogoutView(views.LogoutView):
    template_name = "logged_out.html"


class PasswordChangeView(views.PasswordChangeView):
    template_name = "password_change_form.html"


class PasswordChangeDoneView(views.PasswordChangeDoneView):
    template_name = "password_change_done.html"


class PasswordResetView(views.PasswordResetView):
    template_name = "password_reset_form.html"


class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = "password_reset_done.html"


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = "password_reset_confirm.html"


class PasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = "password_reset_complete.html"
