# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from dataentry.models import Questionnaire, Questionntp2, Reponsentp2, Personne, Resultatntp2, Resultatrepetntp2, Etablissement, Municipalite
# from dataentry.models import Victime, Typequestion, Listevaleur
from django.conf import settings
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse, StreamingHttpResponse
from dataentry.dataentry_constants import CHOIX_ONUK

import datetime


DATE = datetime.datetime.now().strftime('%Y %b %d')

# Pour exportation en CSV
class Echo(object):
    # An object that implements just the write method of the file-like interface.
    def write(self, value):
        # Write the value by returning it, instead of storing in a buffer
        return value

@login_required(login_url=settings.LOGIN_URI)
def verifie_csv(request, pid):
    # Pour exporter les données de base (les questions qui ont l'attribu qstyle=1 pour tous les cas
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exportation.txt"'
    province = request.user.profile.province

    personne = Personne.objects.get(pk=pid)
    csv_data = ([])
    debut = []
    debut.append('Province & File code')
    debut.append(personne.province.reponse_en)
    debut.append(personne.code)
    csv_data.append(debut)
    questionnaires = Questionnaire.objects.filter(id__gt=1 )
    for questionnaire in questionnaires:
        questions = Questionntp2.objects.filter(qstyle=1, questionnaire_id=questionnaire.id).order_by('questionno')
        ligne2 = []
        ligne2.append(questionnaire.nom_en)
        csv_data.append(ligne2)
        if questionnaire.id < 2000:
            for question in questions:
                ligne = []
                ligne.append(question.varname)
                ligne.append(question.questionen)
                donnee = Resultatntp2.objects.filter(personne__id=pid, question__id=question.id, assistant__id=request.user.id, )
                if donnee:
                    reponse = fait_reponse(donnee[0].reponsetexte, question, province)
                    ligne.append(reponse)
                else:
                    ligne.append('-')
                csv_data.append(ligne)
        else:
            donnees = Resultatrepetntp2.objects.order_by().filter(personne__id=pid, assistant__id=request.user.id, questionnaire__id=questionnaire.id).values_list('fiche', flat=True).distinct()
            compte = donnees.count()
            ligne2 = []
            ligne2.append(str(compte) + ' different ' + questionnaire.nom_en)
            csv_data.append(ligne2)
            fait_repetitives(csv_data, donnees, pid, province, questions, request)

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer,dialect="excel-tab")
    response = StreamingHttpResponse((writer.writerow(row) for row in csv_data),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="' + str(personne.code) + '.txt"'
    return response


def fait_repetitives(csv_data, donnees, pid, province, questions, request):
    for i in donnees:
        ligne2 = []
        ligne2.append('Hospitalization card number ' + str(i))
        csv_data.append(ligne2)
        for question in questions:
            ligne = []
            ligne.append(question.varname)
            ligne.append(question.questionen)
            donnee = Resultatrepetntp2.objects.filter(personne__id=pid, question_id=question.id,
                                                      assistant__id=request.user.id, fiche=i)
            if donnee:
                reponse = fait_reponse(donnee[0].reponsetexte, question, province)
                ligne.append(reponse)
            else:
                ligne.append('-')
            csv_data.append(ligne)


def fait_reponse(reponsetexte, question, province):
    if question.typequestion.nom == 'CATEGORIAL':
        resultat = Reponsentp2.objects.get(question=question.id,reponse_valeur=reponsetexte).__str__()
    elif question.typequestion.nom == 'DICHO' or question.typequestion.nom  == 'DICHOU':
        resultat = CHOIX_ONUK[int(reponsetexte)]
    elif question.typequestion.nom == 'ETABLISSEMENT':
        resultat = Etablissement.objects.get(province__id=province,reponse_valeur=reponsetexte).__str__()
    elif question.typequestion.nom == 'MUNICIPALITE':
        resultat = Municipalite.objects.get(province__id=province, reponse_valeur=reponsetexte).__str__()
    else:
        resultat = reponsetexte
    return resultat


@login_required(login_url=settings.LOGIN_URI)
def ffait_csv(request):
    # Pour exporter les données de base (les questions qui ont l'attribu qstyle=1 pour tous les cas
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    questions = Questionntp2.objects.filter(qstyle=1).order_by('questionnaire_id','questionno')
    personnes = Personne.objects.all()
    toutesleslignes = ([])
    #writer = csv.writer(response)
    entete = []
    entete.append('ID')
    for question in questions:
       entete.append(question.varname)

    #writer.writerow(entete)
    toutesleslignes.append(entete)
    for personne in personnes:
        ligne = [personne.code]
        for question in questions:
            donnee = Resultatntp2.objects.filter(pk=personne.id, question_id=question.id,assistant_id=1,)
            if donnee:
                ligne.append(donnee[0].reponsetexte)
            else:
                ligne.append('-')

        toutesleslignes.append(ligne)
        #writer.writerow([donnee for donnee in ligne])

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in toutesleslignes),
                                     content_type="text/csv")
    response['donnes'] = 'attachment; filename="donnes.csv"'
    return response




