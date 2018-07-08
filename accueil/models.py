from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
import datetime
now = datetime.datetime.now()

##Pour les utilisateurs
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


##Pour le logging
class AuditEntree(models.Model):

    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    username =  models.CharField(max_length=256, null=True)
    logintime = models.DateTimeField(null=True)
    logouttime = models.DateTimeField(null=True)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):

    ip = request.META.get('REMOTE_ADDR')
    AuditEntree.objects.create(action='user_logged_in', ip=ip, username=user.username, logintime = now)


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):

    ip = request.META.get('REMOTE_ADDR')
    AuditEntree.objects.create(action='user_logged_out', ip=ip, username=user.username, logouttime = now)


@receiver(user_login_failed)
def user_login_failed_callback(sender, request, credentials, **kwargs):

    ip = request.META.get('REMOTE_ADDR')
    AuditEntree.objects.create(action='user_login_failed', ip=ip, username=credentials.get('username', None))


##Pour les publications
class Affichage(models.Model):
    nom = models.CharField(max_length=250,)

    def __str__(self):
        return '%s' % self.nom


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


