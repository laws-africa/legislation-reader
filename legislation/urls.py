from django.urls import path
from reader.views import *

urlpatterns = [
    path('', WorkListView.as_view(), name="home"),
    # the FRBR URI starts with a /
    path('expression<path:frbr_uri>', ExpressionDetailView.as_view(), name="expression"),
]
