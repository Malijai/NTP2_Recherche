# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from reportlab.pdfgen.canvas import Canvas
from django.core.files.storage import FileSystemStorage
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from django.contrib.auth.decorators import login_required
import datetime
# A necessite l'installation de reportlab (pip install reportlab)
from accueil.models import Tempsfacture


NOM_FICHIER_PDF = "FeuilleTemps.pdf"
PAGE_INFO = "Feuilles de temps - Date d'impression : " + datetime.datetime.now().strftime('%d/%m/%Y')
DATE = datetime.datetime.now().strftime('%Y %b %d')


@login_required(login_url=settings.LOGIN_URI)
def fdetemps(request):
    semaines = [0, 1]
    jours = {
        0: {'nom': "Dimanche", 'semaines': semaines},
        1: {'nom': "Lundi", 'semaines': semaines},
        2: {'nom': "Mardi", 'semaines': semaines},
        3: {'nom': "Mercredi", 'semaines': semaines},
        4: {'nom': "Jeudi", 'semaines': semaines},
        5: {'nom': "Vendredi", 'semaines': semaines},
        6: {'nom': "Samedi", 'semaines': semaines},
        }
    img = ImageReader('dataentry/Feuilledetemps.jpg')
    x = 5
    y = 5
    w = 600
    h = 750
    fichier = NOM_FICHIER_PDF
    #    doc = SimpleDocTemplate("/tmp/{}".format(NOM_FICHIER_PDF))
    if request.method == 'POST':
        y_sign = 615
        xjour = [
            [113, 138, 163, 188, 213, 238, 263],
            [299, 324, 348, 372, 396, 420, 445]
        ]
        y_heures = 418
        y_dates = 440
        somme_temps = 0

        date1 = request.POST.get('date')
        if date1 == "":
            messages.add_message(request, messages.ERROR, "Vous devez rentrer une date")
            return render(request, 'fdt.html', {'jours': jours})

        mois, jour, an = date1.split('/')
        maintenant = datetime.date(int(an), int(mois), int(jour))
        semaine = maintenant.strftime("%U")
        if int(semaine) % 2 > 0:
            d = str(an) + "-W" + semaine
            debut = datetime.datetime.strptime(d + '-0', "%Y-W%W-%w")
        else:
            semcorr = int(semaine) - 1
            d = str(an) + "-W" + str(semcorr)
            debut = datetime.datetime.strptime(d + '-0', "%Y-W%W-%w")
        fin = debut + datetime.timedelta(days=13)
        quinzaine = (float(maintenant.strftime("%U")) + 4) / 2

        if int(maintenant.strftime("%U")) % 2 > 0:
            quinzaine = int(quinzaine + 1)
        if quinzaine > 26:
            quinzaine = int(quinzaine - 26)

        date_debut = debut.strftime("%d-%m-%Y")
        date_fin = fin.strftime("%d-%m-%Y")

        doc = Canvas("/tmp/{}".format(fichier), pagesize=letter)
        doc.drawImage(img, x, y, w, h)
        doc.setFont('Helvetica', 10)
        doc.drawString(10, 10, PAGE_INFO)
        doc.drawString(330, y_sign, request.user.contrat.numeemploye)
        doc.setFont('Helvetica', 12)
        doc.drawString(70, 750, 'No contrat : ' + request.user.contrat.numcontrat)
        doc.drawString(290, 750, 'No budget : ' + request.user.contrat.numbudget)
        doc.drawString(70, 636, request.user.first_name.capitalize() + " " + request.user.last_name.capitalize())
        if request.user.contrat.signature:
            signature = ImageReader(request.user.contrat.signature)
            doc.drawImage(signature, 110, (y_sign - 10), 110, 50, mask='auto')

        doc.drawString(450, 645, 'PAIE : ' + str(quinzaine))
        doc.drawString(420, y_sign, date_debut)
        doc.drawString(515, y_sign, date_fin)

        for semaine in semaines:
            temps_semaine = 0
            for jour in range(7):
                x = xjour[semaine][jour]
                val = request.POST.get("{}_{}".format(semaine, jour))
                doc.drawString(x, y_heures, val)
                somme_temps += float(val)
                temps_semaine += float(val)
                if semaine == 1:
                    ecart = jour + 7
                else:
                    ecart = jour
                newdate = debut + datetime.timedelta(days=ecart)
                doc.drawString(x, y_dates, newdate.strftime("%d"))
                if temps_semaine > float(request.user.contrat.maxheures):
                    messages.add_message(request, messages.ERROR, "Nombre maximum d'heures autorisé : " + request.user.contrat.maxheures)
                    return render(request, 'fdt.html', {'jours': jours})

        doc.drawString(515, y_heures, str(somme_temps))

        Tempsfacture.objects.update_or_create(user=request.user, periode=quinzaine,
                                              defaults={'heures': somme_temps, }
                                              )
        doc.save()
        fs = FileSystemStorage("/tmp")
        with fs.open(fichier) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(fichier)
        return response
    else:
        return render(request, 'fdt.html', {'jours': jours})
