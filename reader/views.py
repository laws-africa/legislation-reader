from django.views.generic import ListView, DetailView
from .models import Work, Expression


class WorkListView(ListView):
    model = Work


class ExpressionDetailView(DetailView):
    model = Expression
    slug_field = 'frbr_uri'
    slug_url_kwarg = 'frbr_uri'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get all the other expressions on this expression's work
        context['siblings'] = self.object.work.expressions.exclude(frbr_uri=self.object.frbr_uri)
        return context
