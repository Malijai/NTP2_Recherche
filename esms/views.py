# -*- coding: utf-8 -*-
from django.shortcuts import render
from esms.esms_constants import CHOIX_FINAL, EXPLICATIONSFR, EXPLICATIONSEN, CHOIXEN,CHOIXFR


# Create your views here.


def Faitinstitution(request, choix='', histoire=''):
    # 'b': {'name': 'Génériques aigus', 'choices': ['c', 'd']},

    #if langue == 'FR':
    CHOIX = CHOIXFR
    EXPLICATIONS = EXPLICATIONSFR
    #else:
    #    CHOIX = CHOIXEN
    #    EXPLICATIONS = EXPLICATIONSEN

    liste =('z','o','x','qq')
    if not choix:
        entrees =  [(c, CHOIX[c]['name'], EXPLICATIONS[c]) for c in liste]

        return render(
            request,
            'essaiesms.html',
                    {'choisi': '',
                     'choixs': '',
                     'choixprecedent': '',
                     'historiques': '',
                     'dernier': '',
                     'dernier2': '',
                     'entrees': entrees,
                     }
            )
    else:
        choisi = CHOIX[choix]['name']
        choixs = []
        historiques = []
        choixprecedent = histoire + choix
        dernier=''
        dernier2=''
        if len(CHOIX[choix]['choices']) > 0:
            choixs = [(c, CHOIX[c]['name'],EXPLICATIONS[c]) for c in CHOIX[choix]['choices']]
        else:
            dernier = choisi
            dernier2 = CHOIX_FINAL[choixprecedent]

        for a in histoire:
            if a == choix:
                dernier = CHOIX_FINAL[histoire]
            else:
                historiques.append(CHOIX[a]['name'])

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
                     'dernier2': dernier2,
                     'entrees': '',
                     }
                )