# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from esms.esms_constants import CHOIX_FINAL, EXPLICATIONSFR, EXPLICATIONSEN, CHOIXEN, CHOIXFR
from .forms import RessourceFormSet, RessourceForm, EsmsForm
from .models import Ressource, Equipe, Esms
from django.views import generic
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.utils import translation


from esms.paginationalpha import NamePaginator


@login_required(login_url=settings.LOGIN_URI)
def Faitinstitution(request, pk, choix='', histoire=''):
    # 'b': {'name': 'Génériques aigus', 'choices': ['c', 'd']},
    langue = translation.get_language()

    if langue == 'fr':
        CHOIX = CHOIXFR
        EXPLICATIONS = EXPLICATIONSFR
    else:
        CHOIX = CHOIXEN
        EXPLICATIONS = EXPLICATIONSEN
    ressource = Ressource.objects.get(pk=pk)
    liste = ('z', 'o', 'x', 'qq', 'rr', 'ss')
    if not choix:
        entrees = [(c, CHOIX[c]['name'], EXPLICATIONS[c]) for c in liste]
        return render(
            request,
            'classification_esms.html',
                {'choisi': '',
                 'choixs': '',
                 'choixprecedent': '',
                 'historiques': '',
                 'dernier': '',
                 'dernier2': '',
                 'entrees': entrees,
                 'ressource': ressource,
                 'langue': langue
                 }
            )
    else:
        choisi = CHOIX[choix]['name']
        choixs = []
        historiques = []
        choixprecedent = histoire + choix
        dernier = ''
        dernier2 = ''
        code = ''
        if len(CHOIX[choix]['choices']) > 0:
            choixs = [(c, CHOIX[c]['name'], EXPLICATIONS[c]) for c in CHOIX[choix]['choices']]
        else:
            dernier = choisi
            dernier2 = CHOIX_FINAL[choixprecedent]
            code = choixprecedent
        for a in histoire:
            if a == choix:
                dernier = CHOIX_FINAL[histoire]
            else:
                historiques.append(CHOIX[a]['name'])
        if dernier:
            if request.method == 'POST':
                form = EsmsForm(request.POST)
                if form.is_valid():
                    codeder = form.save(commit=False)
                    codeder.ressource = ressource
                    codeder.code = request.POST.get('code')
                    codeder.save()
                    messages.add_message(request, messages.WARNING, ressource.nom + ' has been coded ' + dernier2)

                    return redirect('listeressources')

        return render(
                    request,
                    'classification_esms.html',
                    {'choisi': choisi,
                     'choixs': choixs,
                     'choixprecedent': choixprecedent,
                     'historiques': historiques,
                     'dernier': dernier,
                     'dernier2': dernier2,
                     'entrees': '',
                     'ressource': ressource,
                     'code': code,
                     'esms_form': EsmsForm()
                     }
                )


@login_required(login_url=settings.LOGIN_URI)
def ressource_new(request):
    entete = "Nouvelle ressource"
    if request.method == "POST":
        form = RessourceForm(request.POST)
        prof_instances = RessourceFormSet(request.POST)

        if form.is_valid() and prof_instances.is_valid():
            entree = form.save(commit=False)
            entree.author = request.user
            entree.save()
            # Now save the data for each form in the formset
            new_prof = []

            for prof_form in prof_instances:
                profession = prof_form.cleaned_data.get('profession')
                nombre = prof_form.cleaned_data.get('nombre')
                tache = prof_form.cleaned_data.get('tache')
                duree = prof_form.cleaned_data.get('duree')

                if profession:
                    new_prof.append(Equipe(ressource=entree, profession=profession, nombre=nombre, tache=tache, duree=duree))
            try:
                with transaction.atomic():
                    # Replace the old with the new
                    Equipe.objects.filter(ressource=entree).delete()
                    Equipe.objects.bulk_create(new_prof)

                    # And notify our users that it worked
                    messages.success(request, "L'équipe est enregistrée.")

            except IntegrityError:  # If the transaction failed
                messages.error(request, "Il y a une erreur dans l'enregistrement de l'equipe.")
                ress_form = RessourceForm()
                prof_formset = RessourceFormSet()
                context = {
                    'form': ress_form,
                    'prof_formset': prof_formset,
                    'entete': entete
                }
                return render(request, "ressource_edit.html", context)
            return redirect('ressource_detail', entree.id)
        else:
            ress_form = RessourceForm()
            prof_formset = RessourceFormSet()
            context = {
                'form': ress_form,
                'prof_formset': prof_formset,
                'entete': entete
            }
            return render(request, "ressource_edit.html", context)
    else:
        #  return render(request, "entree_edit.html", {'form': form, 'tags':tag_list, 'groupes':group_list,})
        ress_form = RessourceForm()
        prof_formset = RessourceFormSet()
        context = {
            'form': ress_form,
            'prof_formset': prof_formset,
            'entete': entete
        }
        return render(request, "ressource_edit.html", context)


class RessourceDetail(generic.DetailView):
    template_name = 'ressource_detail.html'
    model = Ressource


@login_required(login_url=settings.LOGIN_URI)
def rlisting(request):
    ressource_list = Ressource.objects.all()

    paginator = NamePaginator(ressource_list, on="nom", per_page=5)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        page = paginator.page(page)
    except (InvalidPage):
        page = paginator.page(paginator.num_pages)

    return render(request, 'ressources_list.html', {'page': page})


@login_required(login_url=settings.LOGIN_URI)
def ressource_edit(request, pk):
    ressource = Ressource.objects.get(id=pk)
    entete = "Mise a jour de la ressource " + ressource.nom
    if request.method == "POST":
        form = RessourceForm(request.POST, instance=ressource)
        prof_instances = RessourceFormSet(request.POST or None, instance=ressource)
        if form.is_valid():
            entree = form.save(commit=False)
            entree.author = request.user
            entree.save()
            # Now save the data for each form in the formset
            if prof_instances.is_valid():
                new_prof = []
                for prof_form in prof_instances:
                    profession = prof_form.cleaned_data.get('profession')
                    nombre = prof_form.cleaned_data.get('nombre')
                    tache = prof_form.cleaned_data.get('tache')
                    duree = prof_form.cleaned_data.get('duree')

                    if profession:
                        new_prof.append(Equipe(ressource=entree, profession=profession, nombre=nombre, tache=tache, duree=duree))
                try:
                    with transaction.atomic():
                        # Replace the old with the new
                        Equipe.objects.filter(ressource=entree).delete()
                        Equipe.objects.bulk_create(new_prof)

                        # And notify our users that it worked
                        messages.success(request, 'You have updated the resource infos.')

                except IntegrityError:  # If the transaction failed
                    messages.error(request, 'There was an error saving the resource infos.')
                    ress_form = RessourceForm()
                    prof_formset = RessourceFormSet()
                    context = {
                        'form': ress_form,
                        'prof_formset': prof_formset,
                    }
                    return render(request, "ressource_edit.html", context)
            return redirect('ressource_detail', pk)
        else:
            ress_form = RessourceForm(instance=ressource)
            prof_formset = RessourceFormSet(instance=ressource)
            messages.error(request, 'Erreur')

            context = {
                'form': ress_form,
                'prof_formset': prof_formset,
            }
            return render(request, "ressource_edit.html", context)
    else:
        #  return render(request, "entree_edit.html", {'form': form, 'tags':tag_list, 'groupes':group_list,})
        ress_form = RessourceForm(instance=ressource)
        prof_formset = RessourceFormSet(instance=ressource)
        context = {
            'form': ress_form,
            'prof_formset': prof_formset,
            'entete': entete
        }
        return render(request, "ressource_edit.html", context)
