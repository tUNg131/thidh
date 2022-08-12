from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView

from .models import PastPaper, PaperHistory
from .forms import PaperForm


class DoPaperView(LoginRequiredMixin, SingleObjectMixin, FormView):
    record_model = PaperHistory
    model = PastPaper
    form_class = PaperForm
    template_name = "do-paper.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.record = self.get_or_instantiate_record(paper=self.object, user=request.user)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.record = self.get_or_instantiate_record(paper=self.object, user=request.user)
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'record': self.record
        })
        return kwargs

    def get_or_instantiate_record(self, paper, user):
        queryset = self.record_model._default_manager.filter(
            paper_id=paper.id, user_id=user.id, correct_option_count__isnull=True)
        try:
            record = queryset.get()
        except queryset.model.DoesNotExist:
            record = self.record_model(paper=paper, user=user)
        return record

    def form_valid(self, form):
        breakpoint()