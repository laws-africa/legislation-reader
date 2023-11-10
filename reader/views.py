from django.views.generic import ListView, DetailView
from .models import Work, Expression


class WorkListView(ListView):
    model = Work


class ExpressionDetailView(DetailView):
    model = Expression
    slug_field = 'frbr_uri'
    slug_url_kwarg = 'frbr_uri'
