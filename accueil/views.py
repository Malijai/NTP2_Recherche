# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from accueil.models import Publication, Affichage, Projet, Profile
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required


def accueil(request):
    return render(request,'indexrech.html')


def publications(request):
    pasaffiche = Affichage.objects.get(nom='Non')
    publications = Publication.objects.filter(~Q(affichage__id=pasaffiche.id))
    return render(request, 'publications.html',
                      {
                          'publications': publications,
                      }
                  )


def equipe(request):
    return render(request, 'equipe.html')


def resultats(request):
    return render(request, 'resultats.html')


@login_required(login_url=settings.LOGIN_URI)
def entreesystemes(request):
    GH = False
    NTP1 = False
    NTP2 = False
    droits = Projet.objects.filter(user_id=request.user.id)

    for droit in droits:
        if droit.projet == Projet.GH:
            GH = True
        elif droit.projet == Projet.NTP1:
            NTP1 = True
        elif droit.projet == Projet.NTP2:
            NTP2 = True
        elif droit.projet == Projet.ALL:
            GH = True
            NTP1 = True
            NTP2 = True

    return render(request, "entreesystemes.html",
                      {
                        'GH': GH,
                        'NTP1': NTP1,
                        'NTP2': NTP2,
                        'Profile': Profile
                      })
