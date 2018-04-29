from django.conf.urls import url

from . import views
from .views import accueil,publications, equipe, resultats

urlpatterns = [
    url(r'^$', accueil, name='accueil'),
    url(r'^equipe$', equipe, name='equipe'),
    url(r'^resultats$', resultats, name='resultats'),
    url(r'^publications$', publications, name='publications'),
]

#url(r'^new/$', creerdossier, name='creerdossier'),
