# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from .models import Ressource, Equipe, Esms
from django.forms import inlineformset_factory


class EsmsForm(forms.ModelForm):
    class Meta:
        model = Esms
        fields = ('nombre', 'clientele', 'autreinfo')


class RessourceForm(forms.ModelForm):
    class Meta:
        model = Ressource
        exclude = ('author',)


class EquipeForm(forms.ModelForm):
    class Meta:
        model = Equipe
        exclude = ()


RessourceFormSet = inlineformset_factory(Ressource, Equipe, form=RessourceForm,
                                         extra=3, can_delete=True)

