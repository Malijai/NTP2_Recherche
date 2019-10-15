from django.urls import path
from .views import accueil, publications, equipe, resultats, entreesystemes

urlpatterns = [
    path('', accueil, name='accueil'),
    path('equipe', equipe, name='equipe'),
    path('resultats', resultats, name='resultats'),
    path('publications', publications, name='publications'),
    path('datas', entreesystemes, name='entreesystemes'),
]

