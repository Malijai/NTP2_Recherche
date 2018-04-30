# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from accueil.models import Publication, Affichage
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
    return render(request, "entreesystemes.html")
