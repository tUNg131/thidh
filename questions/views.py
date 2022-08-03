from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView
from django.views.generic import ListView

from .models import Paper
from .forms import PaperForm


class PaperDetailView(LoginRequiredMixin, SingleObjectMixin, FormView):
    # Need to check the prefetch_related. https://stackoverflow.com/questions/19649370/django-can-you-tell-if-a-related-field-has-been-prefetched-without-fetching-it
    model = Paper
    template_name = 'paper_details.html'
    form_class = PaperForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.object:
            kwargs.update({
                'paper': self.object
            })
        return kwargs

    def form_valid(self, form):
        form.full_check()
        return self.render_to_response(self.get_context_data(form=form))


class PaperListView(LoginRequiredMixin, ListView):
    model = Paper
    template_name = "paper_list.html"