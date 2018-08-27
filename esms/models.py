from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models


class Ressource(models.Model):
    nom = models.CharField(max_length=200,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.nom


