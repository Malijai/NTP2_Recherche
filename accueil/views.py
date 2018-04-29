# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from accueil.models import Publication, Affichage
from django.db.models import Q

def isManitoba(http_host):
   return True if 'ntpmb.ca' in http_host else False
   #return True


def isMalijai(http_host):
   #return True if 'malijai.org' in http_host else False
   return True


def accueil(request):
    if isManitoba(request.META.get('HTTP_HOST')):
        return render(request,'logged_out.html')
    elif isMalijai(request.META.get('HTTP_HOST')):
        return render(request,'indexrech.html')
    else:
        return render(request, "index.html")


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
