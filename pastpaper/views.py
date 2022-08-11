from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.http import Http404

from .models import PastPaper, PaperHistory


class DoPaperView(LoginRequiredMixin, FormView):
    paper_model = PastPaper
    history_model = PaperHistory

    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        self.paper = self.get_paper()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.paper = self.get_paper()
        return super().post(request, *args, **kwargs)

    def get_paper(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is None:
            raise AttributeError("Paper pk is missing from URLconf")
        queryset = self.paper._default_manager.filter(pk=pk)
        try:
            # Get the single item from the filtered queryset
            paper = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("Paper not found.")
        return paper


