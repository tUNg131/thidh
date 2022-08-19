from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import BaseUpdateView, SingleObjectTemplateResponseMixin
from django.views.generic import TemplateView

from .models import PastPaper, PaperHistory
from .forms import PaperForm


class DoPaperView(LoginRequiredMixin, SingleObjectTemplateResponseMixin, BaseUpdateView):
    paper_model = PastPaper
    model = PaperHistory
    form_class = PaperForm
    template_name = "do-paper.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object_or_none()
        return super(BaseUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object_or_none()
        return super(BaseUpdateView, self).post(request, *args, **kwargs)

    def get_paper(self):
        return self.get_object(queryset=self.paper_model._default_manager.all())

    def get_object_or_none(self):
        self.paper = self.get_paper()

        paper_id = self.paper.id
        user_id = self.request.user.id
        queryset = self.model._default_manager.filter(
            paper_id=paper_id,
            user_id=user_id,
            correct_option_count__isnull=True
        )
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            obj = None
        return obj

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "paper": self.paper,
            "user": self.request.user,
        })
        return kwargs


class TestView(TemplateView):
    template_name = "test.html"


class TestFormView(TemplateView):
    template_name = "form.html"
