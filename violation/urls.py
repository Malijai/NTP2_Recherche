from django.conf.urls import url
from .views import rechercher
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', rechercher, name='Rechercherviol'),
    url(r'listevcc.html', TemplateView.as_view(template_name="listevcc.html"), name='listevccs'),
]

