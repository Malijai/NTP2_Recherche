from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.apps import apps
from .models import NouveauxDelitsntp1, Personnegrcntp1, Municipalite, Liberationntp1, Province
from django.contrib import messages
from .forms import PersonneForm, NouveauxDelitsForm, LiberationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import translation
from django.utils.translation import gettext_lazy as _
#from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, StreamingHttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
# A necessite l'installation de reportlab (pip install reportlab)
import datetime
import csv

# from django.db import connection

NOM_FICHIER_PDF = "RCMP_Dictionary.pdf"
TITRE = "RCMP Vairiable list"
PAGE_INFO = "RCMP Data protocol - Printed date: " + datetime.datetime.now().strftime('%Y/%m/%d')
PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]
styles = getSampleStyleSheet()
DATE = datetime.datetime.now().strftime('%Y %b %d')
ENTETE = "RCMP Data protocol"


@login_required(login_url=settings.LOGIN_URI)
def choix_province(request):
    entete = ENTETE + " : Choix de la province"
    provinces = Province.objects.all()
    if request.method == 'POST':
        return redirect(liste_personne, request.POST.get('provinceid') )
    else:
        return render(request, 'choixprovince.html', {'provinces': provinces, 'entete': entete})


## Affiche la liste des dossiers encore ouverts
@login_required(login_url=settings.LOGIN_URI)
def liste_personne(request, pi):
    entete = ENTETE + " : Listing"
    personne_list = Personnegrcntp1.objects.filter(Q(ferme=0) & Q(province=pi))
    paginator = Paginator(personne_list, 100)
    page = request.GET.get('page')
    try:
        personnes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        personnes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        personnes = paginator.page(paginator.num_pages)
    return render(request, 'listentp1.html', {'personnes': personnes, 'entete': entete})


## Pour clore les dossiers terminés
@login_required(login_url=settings.LOGIN_URI)
def personne_ferme(request, pk):
    personne = Personnegrcntp1.objects.get(pk=pk)
    personne.ferme = 1
    personne.save()
    messages.success(request, "Fermeture de " + str(personne.codeGRC))
    return redirect(liste_personne, personne.province_id)


@login_required(login_url=settings.LOGIN_URI)
def personne_edit(request, pk):
    langue = translation.get_language()
    personne = Personnegrcntp1.objects.get(pk=pk)
    entete = ENTETE + " : Mise à jour informations individu"
    if request.method == 'POST':
        form = PersonneForm(request.POST, instance=personne)
        if form.is_valid():
            personne = form.save(commit=False)
            personne.RA = request.user
            #print(request.POST.get('dateprint2').__class__)
            newfps = request.POST.get('newpresencefps')
            #print("bbb ", str(newfps))
            if str(newfps) == "None":
                personne.ferme = 1
                personne.save()
                messages.success(request, _(u"Pas de dossier pour cette personne,le dossier a été fermé."))
                return redirect(liste_personne, personne.province_id)
            else:
                if request.POST.get('dateprint2') != "":
                    personne.save()
                    return redirect('personne_delits', personne.id)
                else:
                    messages.error(request, _(u"S'il y a un dossier, il doit y avoir une date d'impression ."))
                    return render(request, "personne_edit.html",
                                  {'my_form': form, 'entete': entete, 'personne': personne})
    else:
        form = PersonneForm(instance=personne)
    return render(request, "personne_edit.html", {'my_form': form, 'entete': entete, 'personne': personne})


## Pour vérifier si de nouveaux délits sont présents dans les fiches
# @login_required(login_url=settings.LOGIN_URI)
# def personne_edit(request, pk):
#     langue = translation.get_language()
#     personne = Personnegrcntp1.objects.get(pk=pk)
#     entete = ENTETE + " : Mise à jour informations individu"
#     date_old_sentence = datetime.date(1900, 1, 1)
#     oldfps = personne.oldpresencefps
#     if NouveauxDelitsntp1.objects.filter(personnegrc=personne).exists():
#         dernieredate = NouveauxDelitsntp1.objects.filter(personnegrc=personne).order_by('-date_sentence').first()
#         date_old_sentence = dernieredate.date_sentence
#
#     if request.method == 'POST':
#         form = PersonneForm(request.POST, instance=personne)
#         if form.is_valid():
#             personne = form.save(commit=False)
#             personne.RA = request.user
#             # print(request.POST.get('dateprint2').__class__)
#             newfps = request.POST.get('newpresencefps')
#             date_new_sentence = datetime.date(1900, 1, 1)
#             if request.POST.get('dateverdictder') != "":
#                 an, mois, jour = request.POST.get('dateverdictder').split('-')
#                 date_new_sentence = datetime.date(int(an), int(mois), int(jour))
#             timediff = date_new_sentence - date_old_sentence
#
#             if timediff.days > 1:
#                 personne.newdelit = 1
#                 messages.success(request, _(u"La personne a été mise à jour."))
#             else:
#                 personne.newdelit = 0
#                 personne.ferme = 1
#                 messages.success(request, _(u"Pas de nouveaux délits, la personne a été mise à jour et le dossier fermé."))
#             personne.save()
#             if (date_new_sentence > date_old_sentence) | (oldfps == 0 and newfps == 1):
#                 return redirect('personne_delits', personne.id)
#             else:
#                 return redirect('liste_personne')
#         else:
#             messages.error(request, _(u"Il y a une erreur dans l'enregistrement"))
#             return redirect('personne_edit', personne.id)
#     else:
#         form = PersonneForm(instance=personne)
#  #       form.fields['dateprint2'].widget = DateTimePickerInput(format='%d/%m/%Y')
#  #       form.fields['dateverdictder'].widget = DateTimePickerInput(format='%d/%m/%Y')
#     return render(request, "personne_edit.html", {'my_form': form, 'entete': entete, 'personne': personne})


## Permet sur une même page d'enregistrer les délits, les libérations et de voir ce qui est déjà rentré
@login_required(login_url=settings.LOGIN_URI)
def personne_delits(request, pk):
    personne = Personnegrcntp1.objects.get(pk=pk)
    delits = NouveauxDelitsntp1.objects.filter(personnegrc=personne).order_by('-date_sentence')
    liberations = Liberationntp1.objects.filter(personnegrc=personne).order_by('-date_liberation')
    entete = ENTETE + " : Délits "
    # Fait la liste des villes de la province correspondante et ajoute les autres
    ville = Municipalite.objects.filter(Q(province=personne.province) | Q(province=10))
    form = NouveauxDelitsForm(prefix='delit')
    form.fields['lieu_sentence'].queryset = ville
    libe_form = LiberationForm(prefix='libe')
    if request.method == 'POST':
        if 'Savelibe' or 'Savelibequit' in request.POST:
            libe_form = LiberationForm(request.POST, prefix='libe')
            form = NouveauxDelitsForm(prefix='delit')
            if libe_form.is_valid():
                libe = libe_form.save(commit=False)
                libe.RA = request.user
                libe.personnegrc = personne
                libe.save()
                messages.success(request, _(u'Une liberation de {} a été ajoutée.').format(personne.codeGRC))
                if 'Savelibequit' in request.POST:
                    return redirect('liste_personne', personne.province_id)
                elif 'Savelibe':
                    return redirect(personne_delits, personne.id)
        if not libe_form.is_valid():
            if 'Savequit' or 'Savedelit' in request.POST:
                form = NouveauxDelitsForm(request.POST, prefix='delit')
                libe_form = LiberationForm(prefix='libe')
                if form.is_valid():
                    delit = form.save(commit=False)
                    delit.RA = request.user
                    delit.personnegrc = personne
                    delit.province = personne.province
                    delit.nouveaudelit = 1
                    delit.save()
                    messages.success(request, _(u'Les delits du #  {} ont été mis à jour.').format(personne.codeGRC))
                    if 'Savequit' in request.POST:
                        return redirect(liste_personne, personne.province_id)
                    else:
                        return redirect(personne_delits, personne.id)
        if not libe_form.is_valid():
            messages.error(request, _(u"Il y a une erreur dans l'enregistrement de la liberation"))
        if not form.is_valid():
            messages.error(request, _(u"Il y a une erreur dans l'enregistrement du delit"))
    return render(request, "personne_delits.html", {'personne': personne,
                                                    'delits': delits,
                                                    'liberations': liberations,
                                                    'form': form,
                                                    'libe_form': libe_form,
                                                    'entete': entete})


# Exportation des questions et variables en PDF
def myFirstPage(patron, _):
    patron.saveState()
    patron.setFont('Helvetica', 16)
    patron.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 108, TITRE)
    patron.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 130, DATE)
    patron.setFont('Helvetica', 10)
    patron.setStrokeColorRGB(0, 0, 0)
    patron.setLineWidth(0.5)
    patron.line(0, 65, PAGE_WIDTH - 0, 65)
    patron.drawString(inch, 0.70 * inch, "RCMP data / %s" % PAGE_INFO)
    patron.restoreState()


def myLaterPages(patron, doc):
    patron.saveState()
    patron.setFont('Helvetica', 10)
    patron.setStrokeColorRGB(0, 0, 0)
    patron.setLineWidth(0.5)
    patron.line(0, 65, PAGE_WIDTH - 0, 65)
    patron.drawString(inch, 0.70 * inch, "Page %d %s" % (doc.page, PAGE_INFO))
    patron.restoreState()


@login_required(login_url=settings.LOGIN_URI)
def do_dico_pdf(request):
    fichier = NOM_FICHIER_PDF
    doc = SimpleDocTemplate("/tmp/{}".format(fichier))
    cs = NouveauxDelitsntp1()
    all_fields = cs._meta.get_fields()

    Story = [Spacer(1, 1.5 * inch)]
    Story.append(Paragraph("RCMP Decisions", styles["Heading1"]))
    Story.append(Spacer(1, 0.5 * inch))
    bullettes = styles['Code']

    Story.append(Paragraph("Variable Name &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data format &nbsp;&nbsp;&nbsp;Question text/Value list",
                           styles["Normal"]))
    for field in all_fields:
        if field.name != 'id' and field.name != 'nouveaudelit' \
                and field.name != 'updated_at' and field.name != 'created_at' and field.name != 'province' \
                and field.name != 'old_RA' and field.name != 'RA':
            verbose = NouveauxDelitsntp1._meta.get_field(field.name).verbose_name
            typef = NouveauxDelitsntp1._meta.get_field(field.name).get_internal_type()
            Story.append(Spacer(1, 0.2 * inch))
            if typef == "DateField" or typef == "IntegerField" or typef == "CharField":
                Story.append(Paragraph(
                    '{}&nbsp;&nbsp;&nbsp;&nbsp;{}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{}'.format(field.name, typef,
                                                                                                verbose),
                    styles["Normal"]))
            else:
                Story.append(Paragraph(
                    '{}&nbsp;&nbsp;&nbsp;&nbsp;Value list&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{}'.format(field.name,
                                                                                                        verbose),
                    styles["Normal"]))
            if typef == "BooleanField":
                liste = [(1, 'Yes'), (0, 'No')]
                for list in liste:
                    espace = '&nbsp;' * 10 + '&#x00B7;'
                    bogustext = '{}&nbsp;{}&nbsp;&nbsp;{}'.format(espace, list[0], list[1])
                    p = Paragraph(bogustext, bullettes)
                    Story.append(p)
            elif typef == "ForeignKey":
                tableL = NouveauxDelitsntp1._meta.get_field(field.name).remote_field.model.__name__
                if tableL != 'Personnegrcntp1' and tableL != 'Province' and tableL != 'User':
                    Tableliee = apps.get_model('NTP1Reprise', tableL)
                    liste = Tableliee.objects.all().order_by('reponse_valeur')
                    espace = '&nbsp;' * 10 + '&#x00B7;'
                    for val in liste:
                        if tableL == 'Municipalite':
                            bogustext = ""
                            #"'{}&nbsp;{}&nbsp;{}&nbsp;&nbsp;{}&nbsp;&nbsp;'.format(espace,
                                                                                              # val.province.reponse_en,
                                                                                              # val.reponse_valeur,
                                                                                              # val.reponse_en, )
                        else:
                            bogustext = '{}&nbsp;{}&nbsp;&nbsp;{}'.format(espace, val.reponse_valeur, val.reponse_en)
                        p = Paragraph(bogustext, bullettes)
                        Story.append(p)
    Story.append(PageBreak())
    Story.append(Paragraph("RCMP Individual data", styles["Heading1"]))

    Story.append(Spacer(1, 0.5 * inch))
    Story.append(Paragraph("I have used an ancient system which was used to update data. So the dateprint1, "
                            " oldpresencefps, delit refers to the "
                           "presence of previously saved data, the other fields refers to the updated variables.",
                           styles["Normal"]))
    Story.append(Spacer(1, 0.2 * inch))

    Story.append(Paragraph("Variable Name &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data format &nbsp;&nbsp;&nbsp;Question text/Value list",
                           styles["Normal"]))
    perso = Personnegrcntp1()
    all_fieldsp = perso._meta.get_fields()
    for field in all_fieldsp:
        if field.name == 'newdelit' or field.name == 'dateprint1' \
                or field.name == 'datedeces' or field.name == 'codeGRC' \
                or field.name == 'dateprint2' or field.name == 'newpresencefps':
            verbose = Personnegrcntp1._meta.get_field(field.name).verbose_name
            typef = Personnegrcntp1._meta.get_field(field.name).get_internal_type()
            Story.append(Spacer(1, 0.2 * inch))
            if typef == "DateField" or typef == "IntegerField" or typef == "CharField":
                Story.append(Paragraph(
                    '{}&nbsp;&nbsp;&nbsp;&nbsp;{}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{}'.format(field.name, typef,
                                                                                                verbose),
                    styles["Normal"]))
            else:
                Story.append(Paragraph(
                    '{}&nbsp;&nbsp;&nbsp;&nbsp;Value list&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{}'.format(field.name,
                                                                                                        verbose),
                    styles["Normal"]))
            if typef == "BooleanField":
                liste = [(1, 'Yes'), (0, 'No')]
                for list in liste:
                    espace = '&nbsp;' * 10 + '&#x00B7;'
                    bogustext = '{}&nbsp;{}&nbsp;&nbsp;{}'.format(espace, list[0], list[1])
                    p = Paragraph(bogustext, bullettes)
                    Story.append(p)
        elif field.name == 'delit' or field.name == 'oldpresencefps':
            verbose = Personnegrcntp1._meta.get_field(field.name).verbose_name
            Story.append(Spacer(1, 0.2 * inch))
            Story.append(Paragraph(
                '{}&nbsp;&nbsp;&nbsp;&nbsp;Value list&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{}'.format(field.name,
                                                                                                    verbose),
                styles["Normal"]))
            liste = [(1, 'Yes'), (0, 'No')]
            for list in liste:
                espace = '&nbsp;' * 10 + '&#x00B7;'
                bogustext = '{}&nbsp;{}&nbsp;&nbsp;{}'.format(espace, list[0], list[1])
                p = Paragraph(bogustext, bullettes)
                Story.append(p)

    Story.append(PageBreak())
    Story.append(Paragraph("RCMP Release informations", styles["Heading1"]))
    Story.append(Spacer(1, 0.5 * inch))
    Story.append(Paragraph("Variable Name &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data format &nbsp;&nbsp;&nbsp;Question text/Value list",
                           styles["Normal"]))
    liber = Liberationntp1()
    all_fieldliber = liber._meta.get_fields()
    for field in all_fieldliber:
        if field.name != 'id' and field.name != 'RA' and field.name != 'updated_at' and field.name != 'created_at':
            verbose = Liberationntp1._meta.get_field(field.name).verbose_name
            typef = Liberationntp1._meta.get_field(field.name).get_internal_type()
            Story.append(Spacer(1, 0.2 * inch))
            if typef == "DateField" or typef == "IntegerField" or typef == "CharField":
                Story.append(Paragraph(
                    '{}&nbsp;&nbsp;&nbsp;&nbsp;{}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{}'.format(field.name, typef,
                                                                                                verbose),
                    styles["Normal"]))
            else:
                Story.append(Paragraph(
                    '{}&nbsp;&nbsp;&nbsp;&nbsp;Value list&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{}'.format(field.name,
                                                                                                        verbose),
                    styles["Normal"]))
            if typef == "BooleanField":
                liste = [(1, 'Yes'), (0, 'No')]
                for list in liste:
                    espace = '&nbsp;' * 10 + '&#x00B7;'
                    bogustext = '{}&nbsp;{}&nbsp;&nbsp;{}'.format(espace, list[0], list[1])
                    p = Paragraph(bogustext, bullettes)
                    Story.append(p)

    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

    fs = FileSystemStorage("/tmp")
    with fs.open(fichier) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(fichier)
    return response


# Pour l'exportation en streaming du CSV
class Echo(object):
    # An object that implements just the write method of the file-like interface.
    def write(self, value):
        # Write the value by returning it, instead of storing in a buffer
        return value


# Toronto: release of justice data for 1 year prior to enrolment and for the next 5 years.
# The Toronto cohort baseline and randomization period lasted 2 years from 2009-2011
# and participants were reconsented at various time points during the 4 year extended study period.
# Unfortunately the linkage period listed on the consent form wasn’t updated so for participants who
# signed a consent form in say 2015 we technically have consent to access their information until 2020.
# For consistency we’ve decided to censor data at March 2017.
def export_csv_sent(request, pi):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exportation.txt"'
    personnes = Personnegrcntp1.objects.filter(province_id=pi).order_by('codeGRC')
    toutesleslignes = []
    ligne = []
    entete = ['personnegrc', 'date_sentence', 'type_tribunal', 'lieu_sentence', 'ordre_delit', 'codeCCdelit',
              'nombre_chefs', 'violation', 'verdict', 'amendeON', 'detentionON', 'probationON', 'interdictionON',
              'surcisON', 'autreON', 'autredetails']
    toutesleslignes.append(entete)
    for personne in personnes:
        debut = personne.enrolmentdate
        bondebut = debut - datetime.timedelta(days=365)
        print(personne.codeGRC, ' -- ', debut, ' -- ', bondebut)

        if NouveauxDelitsntp1.objects.filter(personnegrc=personne).exists():
            donnees = NouveauxDelitsntp1.objects.filter(Q(personnegrc=personne) \
                                             & Q(date_sentence__gte=bondebut) \
                                             & Q(date_sentence__lte=personne.enddate)). \
                order_by('date_sentence')
            for donnee in donnees:
                ligne = [donnee.personnegrc.codeGRC, donnee.date_sentence, donnee.type_tribunal.reponse_valeur,
                         donnee.lieu_sentence.reponse_en, donnee.ordre_delit, donnee.codeCCdelit,
                         donnee.nombre_chefs, donnee.violation.reponse_valeur, donnee.verdict.reponse_en,
                         traduitbool(donnee.amendeON), traduitbool(donnee.detentionON), traduitbool(donnee.probationON),
                         traduitbool(donnee.interdictionON),
                         traduitbool(donnee.surcisON), traduitbool(donnee.autreON), traduitbool(donnee.autredetails)]
                # print(donnee.amendeON)
                toutesleslignes.append(ligne)
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    filename = 'Sentences_Toronto{}.csv'.format(now)
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    response = StreamingHttpResponse((writer.writerow(row) for row in toutesleslignes),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment;  filename="' + filename + '"'
    return response


def traduitbool(val):
    valbool = "-"
    if str(val) == "True":
        valbool = "Yes"
    elif str(val) == "False":
        valbool = "No"
    elif str(val) == "NULL":
        valbool = ""
    else:
        valbool = val
    return valbool


def export_csv_libe(request, pi):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exportation.txt"'
    personnes = Personnegrcntp1.objects.filter(province_id=pi).order_by('codeGRC')
    toutesleslignes = []
    ligne = []
    entete = ['personnegrc', 'date_liberation', 'type']
    toutesleslignes.append(entete)
    for personne in personnes:
        debut = personne.enrolmentdate
        bondebut = debut - datetime.timedelta(days=365)

        if Liberationntp1.objects.filter(personnegrc=personne).exists():
            print(personne.codeGRC, ' -- existe ', personne.id)
            donnees = Liberationntp1.objects.filter(Q(personnegrc=personne) \
                                                & Q(date_liberation__gte=bondebut) \
                                                & Q(date_liberation__lte=personne.enddate)). \
                order_by('date_liberation')
            for donnee in donnees:
                ligne = [donnee.personnegrc.codeGRC, donnee.date_liberation, traduitbool(donnee.type)]
                # print(donnee.amendeON)
                toutesleslignes.append(ligne)
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    filename = 'Liberations_Toronto{}.csv'.format(now)
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    response = StreamingHttpResponse((writer.writerow(row) for row in toutesleslignes),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment;  filename="' + filename + '"'
    return response


def export_csv_dc(request, pi):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exportation.txt"'
    personnes = Personnegrcntp1.objects.filter(province_id=pi).order_by('codeGRC')
    toutesleslignes = []
    ligne = []
    entete = ['personnegrc', 'date_dcd']
    toutesleslignes.append(entete)
    for personne in personnes:
        debut = personne.enrolmentdate
        bondebut = debut - datetime.timedelta(days=365)
        if personne.datedeces:
            if personne.datedeces >= bondebut and personne.datedeces <= personne.enddate:
                ligne = [personne.codeGRC, personne.datedeces]
                # print(donnee.amendeON)
            toutesleslignes.append(ligne)
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    filename = 'DC_Toronto{}.csv'.format(now)
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    response = StreamingHttpResponse((writer.writerow(row) for row in toutesleslignes),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment;  filename="' + filename + '"'
    return response


from django.shortcuts import render

# Create your views here.
