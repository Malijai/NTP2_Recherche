from django.conf.urls import url
from django.urls import include, path
from .views import liste_personne, personne_delits, personne_ferme, do_dico_pdf, personne_edit, choix_province


urlpatterns = [
    path('personne/<int:pk>/edit/', personne_edit, name='personne_edit'),
    path('delits/<int:pk>/', personne_delits, name='personne_delits'),
    path('province', choix_province, name='choix_province'),
    path('<int:pi>/', liste_personne, name='liste_personne'),
    path('ferme/<int:pk>/',personne_ferme, name='personne_ferme'),
    path('do_pdf/', do_dico_pdf, name='do_dico_pdf'),

]