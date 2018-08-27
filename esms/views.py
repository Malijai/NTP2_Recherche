# -*- coding: utf-8 -*-
from django.shortcuts import render
from esms.esms_constants import CHOIX_INSTITUT, CHOIX_FINAL, EXPLICATIONS


# Create your views here.


def Faitinstitution(request, choix='', histoire=''):
    # 'b': {'name': 'Génériques aigus', 'choices': ['c', 'd']},
    if not choix:
        choix='z'
    choisi = CHOIX_INSTITUT[choix]['name']
    choixs = []
    historiques = []
    choixprecedent = histoire + choix
    dernier=''
    dernier2=''
    if len(CHOIX_INSTITUT[choix]['choices']) > 0:
        choixs = [(c, CHOIX_INSTITUT[c]['name'],EXPLICATIONS[c]) for c in CHOIX_INSTITUT[choix]['choices']]
    else:
        dernier = choisi
        dernier2 = CHOIX_FINAL[choixprecedent]

    for a in histoire:
        if a == choix:
            dernier = CHOIX_FINAL[histoire]
        else:
            historiques.append(CHOIX_INSTITUT[a]['name'])

    if dernier:
        choisi =''
        choixs =''
        choixprecedent =''

    return render(
        request,
        'essaiesms.html',
        {'choisi': choisi,
         'choixs': choixs,
         'choixprecedent': choixprecedent,
         'historiques':  historiques,
         'dernier': dernier,
         'dernier2':dernier2,
         }
    )