from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Dossier(models.Model):
    nomdossier = models.CharField(max_length=100)
    comment = models.CharField(max_length=200, blank=True, null=True)
    parentId = models.ForeignKey("self", on_delete=models.DO_NOTHING)

    def __str__(self):
        return '%s' % self.nomdossier

    def __unicode__(self):
        return u'%s' % self.nomdossier

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d/')
    comment = models.CharField(max_length=200, blank=True, null=True)
    dossier = models.ForeignKey(Dossier, on_delete=models.DO_NOTHING)
    nicename = models.CharField(max_length=100, blank=True, null=True)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)
    posted = models.DateTimeField(auto_now_add=True)
