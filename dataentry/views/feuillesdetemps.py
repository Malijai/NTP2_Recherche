# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.template import loader, Context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.apps import apps
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas
from django.core.files.storage import FileSystemStorage
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
#A necessite l'installation de reportlab (pip install reportlab)
from django.contrib.auth.decorators import login_required
import datetime


NOM_FICHIER_PDF = "FeuilleTemps.pdf"
PAGE_INFO = "Feuilles de temps - Date d'impression : " + datetime.datetime.now().strftime('%d/%m/%Y')
DATE = datetime.datetime.now().strftime('%Y %b %d')


@login_required(login_url=settings.LOGIN_URI)
def fdetemps(request):
    semaines = [0, 1]
    img = ImageReader('dataentry/Feuilledetemps.jpg')
    x = 5
    y = 5
    w = 600
    h = 750
    fichier = NOM_FICHIER_PDF
    #    doc = SimpleDocTemplate("/tmp/{}".format(NOM_FICHIER_PDF))
    if request.method == 'POST':
        doc = Canvas("/tmp/{}".format(fichier), pagesize=letter)
        doc.drawImage(img, x, y, w, h)
        doc.setFont('Helvetica', 10)
        doc.drawString(10, 10, PAGE_INFO)
        doc.setFont('Helvetica', 12)
        doc.drawString(70, 750, 'no contrat :')
        doc.drawString(300, 750, 'budget :')

        doc.drawString(70, 636, 'nom')
        doc.drawString(90, 615, 'signature')
        doc.drawString(340, 615, 'no')
        doc.drawString(420, 615, 'date 1')
        doc.drawString(515, 615, 'date 2 ')

        doc.drawString(110, 440, 'D1')
        doc.drawString(135, 440, 'L1')
        doc.drawString(156, 440, 'Ma1')
        doc.drawString(182, 440, 'Me1')
        doc.drawString(213, 440, 'J1')
        doc.drawString(232, 440, 'Ve1')
        doc.drawString(260, 440, 'S1')

        doc.drawString(300, 440, 'D2')
        doc.drawString(325, 440, 'L2')
        doc.drawString(343, 440, 'Ma2')
        doc.drawString(368, 440, 'Me2')
        doc.drawString(395, 440, 'J2')
        doc.drawString(415, 440, 'Ve2')
        doc.drawString(445, 440, 'S2')
        somme = 0
        y_heures = 418
        xjour = [
            [113, 137, 160, 186, 213, 236, 260],
            [300, 325, 345, 368, 395, 415, 445]
        ]
        for semaine in semaines:
            for jour in range(7):
                x = xjour[semaine][jour]
                val = request.POST.get("{}_{}".format(semaine,jour))
                doc.drawString(x, y_heures, val)
                somme += float(val)

        doc.drawString(515, y_heures, str(somme))

        doc.save()

        fs = FileSystemStorage("/tmp")
        with fs.open(fichier) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(fichier)
        return response

    else:

        return render(
        request,
        'fdt.html',
            {
            'jours': {0: {'nom' : "Dimanche", 'semaines': semaines},
                    1: {'nom': "Lundi", 'semaines': semaines},
                    2: {'nom': "Mardi", 'semaines': semaines},
                    3: {'nom': "Mercredi", 'semaines': semaines},
                    4: {'nom': "Jeudi", 'semaines': semaines},
                    5: {'nom': "Vendredi", 'semaines': semaines},
                    6: {'nom' : "Samedi", 'semaines': semaines},
                    }
        }
        )




