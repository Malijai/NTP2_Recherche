from django.conf.urls import url
from django.urls import include, path
from .views import liste_personne, personne_edit, personne_delits, personne_ferme


urlpatterns = [
    path('personne/<int:pk>/edit/', personne_edit, name='personne_edit'),
    path('delits/<int:pk>/', personne_delits, name='personne_delits'),
    path('', liste_personne, name='liste_personne'),
    path('ferme/<int:pk>/',personne_ferme, name='personne_ferme'),
]