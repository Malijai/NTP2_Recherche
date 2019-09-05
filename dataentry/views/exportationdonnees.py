# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from dataentry.models import Questionnaire, Questionntp2, Reponsentp2, Personne, Resultatntp2, Resultatrepetntp2, Etablissement, Municipalite, Province
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from dataentry.dataentry_constants import CHOIX_ONUK, LISTE_PROVINCE
from accueil.models import Projet, Profile
from django.db.models import Q, Count
from django.template import loader
from django.contrib.auth.models import User
import csv
import os
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
def ffait_csv(request, province, questionnaire):
    # Pour exporter les données par province et questionnaire pour tous les cas
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    province_nom = LISTE_PROVINCE[province]
    filename = 'Datas_{}_{}_{}.csv'.format(province_nom, questionnaire, now)
    questions = Questionntp2.objects.\
                        filter(questionnaire_id=questionnaire).\
                        exclude(Q(typequestion=7) | Q(typequestion=100)).\
                        order_by('questionno').values('id', 'varname')
    personnes = Personne.objects.filter(province_id=province).values('id', 'code')

    toutesleslignes = [[]]
    entete = ['ID', 'code', 'Assistant']
    if questionnaire > 1000:
        entete.append('Card')
    for question in questions:
       entete.append(question['varname'])
    usersntp = [{'id': p.user.id} for p in Projet.objects.filter(projet=Projet.NTP2)]
    usersprovince = [{'id': p.user.id} for p in Profile.objects.filter(province=province)]
    liste = [i for i in usersntp for j in usersprovince if i['id'] == j['id']]

    toutesleslignes.append(entete)
    for assistant in liste:
        for personne in personnes:
            decompte = 0
            if questionnaire > 1000:
                donnees = Resultatrepetntp2.objects.order_by(). \
                                        filter(personne_id=personne['id'], assistant_id=assistant['id'], questionnaire_id=questionnaire). \
                                        values_list('fiche', flat=True).distinct()
                if donnees.count() > 0:
                    ligne = []
                    decompte = 0
                    for card in donnees:
                            ligne, decompte = fait_csv_repetitive(personne['id'], personne['code'], assistant['id'], questions, card, questionnaire)
            else:
                if Resultatntp2.objects.filter(personne_id=personne['id'], assistant_id=assistant['id']).exists():
                    ligne = [personne['id'], personne['code'],assistant['id']]
                    for question in questions:
                        try:
                            donnee = Resultatntp2.objects.filter(personne_id=personne['id'], question_id=question['id'],
                                                                 assistant_id=assistant['id']).values('reponsetexte')
                        except Resultatntp2.DoesNotExist:
                            donnee = None
                        if donnee:
                            ligne.append(donnee[0]['reponsetexte'])
                            decompte += 1
                        else:
                            ligne.append('')

            if decompte > 3:
                toutesleslignes.append(ligne)
    with open(os.path.join(settings.MEDIA_DATA, filename), 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        for row in toutesleslignes:
            writer.writerow(row)

    return render(request, 'donneesntp.html', {'filename': filename, 'MEDIA_DATAURL': settings.MEDIA_DATAURL})


def fait_csv_repetitive(personne, code, assistant, questions, card, questionnaire):
    if Resultatrepetntp2.objects.filter(personne_id=personne, assistant_id=assistant, questionnaire_id=questionnaire, fiche=card).exists():
        ligne = [personne, code, assistant, card]
        decompte = 0
        for question in questions:
            try:
                donnee = Resultatrepetntp2.objects.filter(personne_id=personne, assistant_id=assistant, questionnaire_id=questionnaire, question_id=question['id'], fiche=card).\
                                            values('reponsetexte')

            except Resultatrepetntp2.DoesNotExist:
                donnee = None
            if donnee:
                ligne.append(donnee[0]['reponsetexte'])
                decompte += 1
            else:
                ligne.append('')
    return ligne, decompte


def fait_entete_ntp2_spss(request, questionnaire, province):
    response = HttpResponse(content_type='text/csv')
    filename1 = '"enteteSPSS_' + str(questionnaire)  + '.sps"'
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename1)
    questions, usersntp2 = extraction_requete_ntp2(questionnaire)

    t = loader.get_template('spss_ntp2_syntaxe.txt')
    response.write(t.render({'questions': questions, 'users': usersntp2, 'province': province}))
    return response


def fait_entete_ntp2_stata(request, questionnaire, province):
    response = HttpResponse(content_type='text/csv')
    filename1 = '"enteteSTATA_' + str(questionnaire) + '.txt"'
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename1)
    questions, usersntp2 = extraction_requete_ntp2(questionnaire)
    typepresents = Questionntp2.objects.values('typequestion__nom').order_by().filter(questionnaire_id=questionnaire). \
                                            exclude(Q(typequestion=7) | Q(typequestion=100)). \
                                                annotate(tqcount=Count('typequestion__nom'))

    t = loader.get_template('stata_ntp2_syntaxe.txt')
    response.write(t.render({'questions': questions, 'typequestions': typepresents, 'users': usersntp2, 'province': province}))
    return response



def extraction_requete_ntp2(questionnaire):
    questions = Questionntp2.objects.filter(questionnaire_id=questionnaire). \
                                    exclude(Q(typequestion=7) | Q(typequestion=100)). \
                                    order_by('questionno')
    usersntp2 = [{'id': p.user.id, 'username': p.user.username} for p in Projet.objects.filter(projet=Projet.NTP2)]

    return questions,  usersntp2
