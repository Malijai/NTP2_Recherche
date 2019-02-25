# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
#from django.http import HttpResponse
from gh.models import Questionnaire, Personne, Interview, Resultatrepet, Question, Resultat, User
from accueil.models import Projet
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
import datetime
import csv
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
    filename1 = 'data_{}{}_{}.csv'.format(qid, entrevue, now)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exportationtout.txt"'
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
    personnes = Personne.objects.filter(Q(id__lte=75))
    assistants = User.objects.all()
    for personne in personnes:
        for assistant in assistants:
            for entrevue in entrevues:
                if Resultat.objects.filter(personne__id=personne.id, assistant_id=assistant.id, interview_id=entrevue.id).exists():
                    # print(personne.id, ' - ', assistant.id, ' - ', entrevue.id)
                    ligne = []
                    ligne.append(personne.id)
                    ligne.append(assistant.id)
                    ligne.append(entrevue.id)
                    ligne.append(qid)
                    for question in questions:
                        try:
                            donnee = Resultat.objects.get(personne__id=personne.id, assistant_id=assistant.id, interview_id=entrevue.id, question_id=question.id)
                        except Resultat.DoesNotExist:
                            donnee = None
                        if donnee:
                            ligne.append(donnee.reponse_texte)
                        else:
                            ligne.append('')
                    csv_data.append(ligne)

    pseudo_buffer = Echo()
    # writer = csv.writer(pseudo_buffer, dialect="excel-tab")
    writer = csv.writer(pseudo_buffer,  delimiter = '\t',quoting=csv.QUOTE_MINIMAL)
    response = StreamingHttpResponse((writer.writerow(row) for row in csv_data),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename1)
    return response


def fait_entete_spss(request, qid, intid):
    entrevue = "Baseline" if intid == '1' else "FU"
    response = HttpResponse(content_type='text/csv')
    filename1 = '"enteteSPSS_' + str(qid) + entrevue + '.txt"'
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename1)
    phase = 1 if intid == '1' else 2
    q = (~Q(typequestion__id=7) & ~Q(typequestion__id=100) & (Q(phase=phase) | Q(phase=3)) & Q(questionnaire__id=qid))
    questions = Question.objects.filter(q).order_by('questionno')
    usersgh = Projet.objects.filter(projet=Projet.GH)

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
