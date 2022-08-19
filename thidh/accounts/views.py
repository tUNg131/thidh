from django.contrib.auth import views


class LoginView(views.LoginView):
    next_page = "paper-list"
    template_name = "accounts/login.html"


class LogoutView(views.LogoutView):
    template_name = "accounts/logged_out.html"


class PasswordChangeView(views.PasswordChangeView):
    template_name = "accounts/password_change_form.html"


class PasswordChangeDoneView(views.PasswordChangeDoneView):
    template_name = "accounts/password_change_done.html"


class PasswordResetView(views.PasswordResetView):
    template_name = "accounts/password_reset_form.html"


class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"


class PasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"
