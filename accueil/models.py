from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    QC = 1
    ON = 2
    BC = 3
    MB = 4
    AL = 5
    SK = 6
    NS = 7
    NB = 8
    ALL = 10
    PROVINCE_CHOICES = (
                           (QC, 'Quebec'),
                           (ON, 'Ontario'),
                           (BC, 'British-Columbia'),
                           (MB, 'Manitoba'),
                           (AL, 'Alberta'),
                           (SK, 'Saskatchewan'),
                           (NS, 'Nova-Scotia'),
                           (NB, 'New Brunswick'),
                           (ALL, 'All provinces'),
                        )
    user = models.OneToOneField (User, on_delete=models.CASCADE)
    province = models.PositiveSmallIntegerField(choices=PROVINCE_CHOICES, verbose_name="Province", null=True, blank=True)

    def __str__(self):
        return self.user.username


class Projet(models.Model):
    GH = 1
    NTP1 = 2
    NTP2 = 3
    ALL = 10
    PROJETS_CHOICES = (
                           (GH, 'Going Home'),
                           (NTP1, 'National Trajectory Project'),
                           (NTP2, 'NTP2 Community'),
                           (ALL, 'All projects'),
                        )
    user = models.ForeignKey (User, on_delete=models.CASCADE)
    projet = models.PositiveSmallIntegerField(choices=PROJETS_CHOICES, verbose_name="Projets", null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
    instance.profile.save()


class Affichage(models.Model):
    nom = models.CharField(max_length=250,)

    def __str__(self):
        return '%s' % self.nom

    def __unicode__(self):
        return u'%s' % self.nom


class Publication(models.Model):
    titre = models.CharField(max_length=250,)
    reference = models.CharField(max_length=250,)
    auteurs = models.CharField(max_length=250,)
    annee = models.CharField(max_length=50,)
    lien = models.CharField(max_length=250,blank=True, null=True)
    affichage = models.ForeignKey(Affichage, on_delete=models.CASCADE)
    ordre = models.IntegerField()

    class Meta:
       ordering = ['ordre']

    def __str__(self):
        return '%s' % self.titre

    def __unicode__(self):
        return u'%s' % self.titre
