# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
#from django.http import HttpResponse
from gh.models import Questionnaire, Personne, Interview, Resultatrepet, Question, Resultat, User
from accueil.models import Projet
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Min, Max
import datetime
import csv
import os
from django.template import loader
from django.http import HttpResponse, StreamingHttpResponse


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


@login_required(login_url=settings.LOGIN_URI)
def gh_csv_tous(request, qid, intid):
    # Create the HttpResponse object with the appropriate CSV header.
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    entrevue = "Baseline" if intid == '1' else "FU"
    filename = 'Datas_{}{}_{}.csv'.format(qid, entrevue, now)
    questionnaire = Questionnaire.objects.filter(pk=qid)
    if intid == '1':
        entrevues = Interview.objects.filter(pk=1)
    else:
        entrevues = Interview.objects.filter(Q(pk=200) | Q(pk=300))

    phase = 1 if intid == '1' else 2
    q = (~Q(typequestion__id=7) & ~Q(typequestion__id=100) & (Q(phase=phase) | Q(phase=3)) & Q(questionnaire__id=qid))
    questions = Question.objects.filter(q).order_by('questionno')
    csv_data = ([])
    debut = []
    debut.append('personne_ID')
    debut.append('Assistant_ID')
    debut.append('Entrevue_ID')
    debut.append('Questionnaire')
    for question in questions:
        debut.append(question.varname)
    csv_data.append(debut)

    # personnes = Personne.objects.all()
    nbp = Personne.objects.all().count()
    # personnes = Personne.objects.filter(Q(id__lte=75))
    usersghs = Projet.objects.filter(projet=Projet.GH)
    assistants = User.objects.all()
    completed = False
    for assistant in usersghs:
        for entrevue in entrevues:
            personnes = [p['personne'] for p in \
                Resultat.objects.values('personne').filter(
                    assistant__id=assistant.id, interview=entrevue
                ).annotate(pc=Count('personne', distinct=True)) ]
            for personne_id in personnes:
                if Resultat.objects.filter(personne__id=personne_id, assistant__id=assistant.id, interview=entrevue).exists():
                    # print(personne.id, ' - ', assistant.id, ' - ', entrevue.id)
                    ligne = []
                    ligne.append(personne_id)
                    ligne.append(assistant.id)
                    ligne.append(entrevue.id)
                    ligne.append(qid)
                    for question in questions:
                        try:
                            donnee = Resultat.objects.get(personne__id=personne_id, assistant__id=assistant.id, interview=entrevue, question=question)
                        except Resultat.DoesNotExist:
                            donnee = None
                        if donnee:
                            ligne.append(donnee.reponse_texte)
                        else:
                            ligne.append('')
                    csv_data.append(ligne)
    # MEDIA_DATAURL
    with open(os.path.join(settings.MEDIA_DATA, filename), 'w') as f:
        writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        for row in csv_data:
            writer.writerow(row)
    return render(request,'donnee.html',{filename: filename})


def fait_entete_spss(request, qid, intid):
    entrevue = "Baseline" if intid == '1' else "FU"
    response = HttpResponse(content_type='text/csv')
    filename1 = '"enteteSPSS_' + str(qid) + entrevue + '.txt"'
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename1)
    phase = 1 if intid == '1' else 2
    q = (~Q(typequestion__id=7) & ~Q(typequestion__id=100) & (Q(phase=phase) | Q(phase=3)) & Q(questionnaire__id=qid))
    questions = Question.objects.filter(q).order_by('questionno')
    usersgh = [{'id': p.user.id,'username': p.user.username}  for p in Projet.objects.filter(projet=Projet.GH)]

    t = loader.get_template('spss_syntaxe.txt')
    response.write(t.render({'questions': questions, 'users': usersgh}))
    return response


def fait_entete_stata(request, qid, intid):
    entrevue = "Baseline" if intid == '1' else "FU"
    response = HttpResponse(content_type='text/csv')
    filename1 = '"enteteSTATA_' + str(qid) + entrevue + '.txt"'
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename1)
    phase = 1 if intid == '1' else 2
    q = (~Q(typequestion__id=7) & ~Q(typequestion__id=100) & (Q(phase=phase) | Q(phase=3)) & Q(questionnaire__id=qid))
    questions = Question.objects.filter(q).order_by('questionno')
    typepresents = Question.objects.values('typequestion__nom').order_by().filter(q).annotate(tqcount=Count('typequestion__nom'))
    usersgh = Projet.objects.filter(projet=Projet.GH)

    t = loader.get_template('stata_syntaxe.txt')
    response.write(t.render({'questions': questions, 'typequestions': typepresents, 'users': usersgh}))
    return response


@login_required(login_url=settings.LOGIN_URI)
def gh_csv_tousOLD(request, qid, intid):
    # Create the HttpResponse object with the appropriate CSV header.
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    entrevue = "Baseline" if intid == '1' else "FU"
    filename1 = 'data_{}{}_{}.csv'.format(qid, entrevue, now)
    questionnaire = Questionnaire.objects.filter(pk=qid)
    if intid == '1':
        entrevues = Interview.objects.filter(pk=1)
    else:
        entrevues = Interview.objects.filter(Q(pk=200) | Q(pk=300))

    phase = 1 if intid == '1' else 2
    q = (~Q(typequestion__id=7) & ~Q(typequestion__id=100) & (Q(phase=phase) | Q(phase=3)) & Q(questionnaire__id=qid))
    questions = Question.objects.filter(q).order_by('questionno')
    csv_data = ([])
    debut = []
    debut.append('personne_ID')
    debut.append('Assistant_ID')
    debut.append('Entrevue_ID')
    debut.append('Questionnaire')
    for question in questions:
        debut.append(question.varname)
    csv_data.append(debut)

    # personnes = Personne.objects.all()
    nbp = Personne.objects.all().count()
    minid = Personne.objects.all().aggregate(Min('id'))
    maxid = Personne.objects.all().aggregate(Max('id'))
    nbpas = nbp / 10
    for i in (0, nbpas):
        bas = minid['id_min'] + (i * 10)
        haut = minid['id_min'] + (i + 1 * 10)
        personnes = Personne.objects.filter(Q(id__lte=haut) & Q(id__gte=bas))
        compteur = int(request.GET.get('compteur', 0))
        # personnes = Personne.objects.filter(Q(id__lte=75))
        usersghs = Projet.objects.filter(projet=Projet.GH)
        assistants = User.objects.all()
        completed = False
        for assistant in usersghs:
            for entrevue in entrevues:
                for personne in personnes:
                    if Resultat.objects.filter(personne=personne, assistant__id=assistant.id, interview=entrevue).exists():
                        # print(personne.id, ' - ', assistant.id, ' - ', entrevue.id)
                        ligne = []
                        ligne.append(personne.id)
                        ligne.append(assistant.id)
                        ligne.append(entrevue.id)
                        ligne.append(qid)
                        for question in questions:
                            try:
                                donnee = Resultat.objects.get(personne=personne, assistant__id=assistant.id, interview=entrevue, question=question)
                            except Resultat.DoesNotExist:
                                donnee = None
                            if donnee:
                                ligne.append(donnee.reponse_texte)
                            else:
                                ligne.append('')
                            csv_data.append(ligne)
                        if i == ((compteur + 1) * 10) - 1:
                            compteur += 1
                            completed = True
                i += 1
                if completed:
                    break

    file = 'donnees_{}.txt'.format(compteur)
    with open(os.path.join(settings.MEDIA_ROOT, file), 'w') as f:
        writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        for row in csv_data:
            writer.writerow(row)
    response = redirect('gh_csv_tous', qid, intid)
    response['Location'] += '?compteur={}'.format(compteur)
    return response
