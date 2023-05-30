# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from .models import Personnegrcntp1, NouveauxDelitsntp1, Liberationntp1
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput

# Formulaire pour mettre à jour les données de base: présence de nouveaux délits:
class PersonneForm(forms.ModelForm):
    class Meta:
        model = Personnegrcntp1
        fields = ('dateprint2', 'dateverdictder', 'newpresencefps','datedeces')
        exclude = ('codeGRC', 'province', 'delit', 'dateprint1', 'oldpresencefps', 'assistant', 'newdelit')
        widgets = {
                    'dateprint2' : DatePickerInput(),
                    'dateverdictder': DatePickerInput(),
                    'datedeces': DatePickerInput(),
        }

class FermeForm(forms.ModelForm):
    class Meta:
        model = Personnegrcntp1
        fields = ('ferme',)
        exclude = ('codeGRC', 'province', 'delit', 'dateprint1', 'oldpresencefps', 'assistant', 'newdelit','dateprint2', 'dateverdictder', 'newpresencefps')


# Formulaire pour rentrer les nouveaux délits si nécessaire:
class NouveauxDelitsForm(forms.ModelForm):
    class Meta:
        model = NouveauxDelitsntp1
        amendeON = forms.BooleanField(required=True)
        detentionON = forms.BooleanField(required=True)
        probationON = forms.BooleanField(required=True)
        interdictionON = forms.BooleanField(required=True)
        surcisON = forms.BooleanField(required=True)
        autreON = forms.BooleanField(required=True)
        fields = ('date_sentence','lieu_sentence','type_tribunal','ordre_delit','codeCCdelit','nombre_chefs','violation',
                  'verdict','amendeON','detentionON','probationON','interdictionON','surcisON','autreON','autredetails')
        exclude = ('RA', 'created_at', 'updated_at', 'card', 'province', 'personnegrc','nouveaudelit')
        widgets = {
                    'date_sentence' : DatePickerInput(),
                }

# Formulaire pour rentrer les libérations:
class LiberationForm(forms.ModelForm):
    class Meta:
        model = Liberationntp1
        type = forms.BooleanField(required=True)
        fields = ('date_liberation','type')
        exclude = ('RA', 'created_at', 'updated_at')
        widgets = {
                    'date_liberation' : DatePickerInput(),
                }





