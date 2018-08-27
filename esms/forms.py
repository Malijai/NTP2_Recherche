# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms


class ChoixForm(forms.Form):
    your_name = forms.ChoiceField(label='Chose the most appropriate')