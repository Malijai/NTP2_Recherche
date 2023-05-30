from django.db import models
from django.contrib.auth.models import User


## Liste des valeurs des choix de
# Code de violation
class Violation(models.Model):
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    def __str__(self):
        return '%s %s' % (self.reponse_valeur, self.reponse_en)


## Tribunaux
class Tribunal(models.Model):
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    def __str__(self):
        return '%s' % self.reponse_fr


# Verdicts
class Verdict(models.Model):
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    def __str__(self):
        return '%s' % self.reponse_fr


# Provinces
class Province(models.Model):
    reponse_en = models.CharField(max_length=30,)
    reponse_fr = models.CharField(max_length=30,)

    def __str__(self):
        return '%s' % self.reponse_fr


# Municipalites par provinces
class Municipalite(models.Model):
    reponse_valeur = models.CharField(max_length=20)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )
    province = models.ForeignKey(Province, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['reponse_fr']

    def __str__(self):
        return '%s' % self.reponse_fr

class Type(models.Model):
    reponse_valeur = models.CharField(max_length=20)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    class Meta:
        ordering = ['reponse_fr']

    def __str__(self):
        return '%s' % self.reponse_fr


class Duree(models.Model):
    reponse_valeur = models.CharField(max_length=20)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    class Meta:
        ordering = ['reponse_fr']

    def __str__(self):
        return '%s' % self.reponse_fr

## Entrée des données
# Liste de tous les dossiers avec ou sans FPS
class Personnegrcntp1(models.Model):
    codeGRC = models.CharField(max_length=30, verbose_name="ID")
    province = models.ForeignKey(Province, on_delete=models.DO_NOTHING)
    delit = models.IntegerField(default=1, verbose_name="Présence ancien délits",)
    alias = models.IntegerField(default=1, verbose_name="Présence ancien alias",)
    dateprint1 = models.DateField(verbose_name="Ancienne date print",)
    oldpresencefps = models.IntegerField(verbose_name="Présence ancien FPS",)
    dateprint2 = models.DateField(verbose_name="Date print. Laisser vide si pas de fichier (jj/mm/aaaa)", blank=True, null=True)
    newdelit = models.BooleanField(default=1, verbose_name="Présence de délits après la date du dernier verdict rentré",)
    newpresencefps = models.BooleanField(verbose_name="Présence de FPS en 2022/23. Cocher si oui")
    dateverdictder = models.DateField(verbose_name="Date du dernier verdict présent dans la fiche. Laisser vide si pas de fichier (jj/mm/aaaa)", blank=True, null=True)
    ferme = models.BooleanField()
    datedeces = models.DateField(verbose_name="Si décédé indiquer la date ici (jj/mm/aaaa)", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    RA = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)

    class Meta:
        ordering = ['codeGRC']

    def __str__(self):
        return '%s' % self.codeGRC


# Une fiche pour chaque délit de chaque personne.
class NouveauxDelitsntp1(models.Model):
    personnegrc = models.ForeignKey(Personnegrcntp1, on_delete=models.CASCADE, verbose_name="ID")
    date_sentence = models.DateField(verbose_name="Date de la décision (jj/mm/aaaa)")
    type_tribunal = models.ForeignKey(Tribunal, on_delete=models.DO_NOTHING, verbose_name="Type de tribunal")
    lieu_sentence = models.ForeignKey(Municipalite, on_delete=models.DO_NOTHING, verbose_name="Lieu du verdict")
    ordre_delit = models.IntegerField(default=1, verbose_name="Ordre",)
    descriptiondelit = models.CharField(max_length=150, verbose_name="Description du délit", null=True, blank=True)
    codeCCdelit = models.CharField(max_length=50, verbose_name="Code CC du delit (si pas CC preciser de quel code il s agit)")
    nombre_chefs = models.IntegerField(default=1,verbose_name="Nombre de chefs")
    violation = models.ForeignKey(Violation, on_delete=models.DO_NOTHING, verbose_name="Code de violation")
    verdict = models.ForeignKey(Verdict, related_name='verdict', on_delete=models.DO_NOTHING, verbose_name="Verdict")
    amendeON = models.BooleanField(verbose_name="Amende? Cocher si oui")
    amende_type =  models.ForeignKey(Type, on_delete=models.DO_NOTHING, verbose_name="Caractéristiques de l'amende",null=True, blank=True)
    amendecout = models.CharField(max_length=50, verbose_name="Cout total de l'amende", null=True, blank=True)
    detentionON = models.BooleanField(verbose_name="Détention? Cocher si oui")
    detentionduree = models.CharField(max_length=50, verbose_name="Durée de la détention", null=True, blank=True)
    unitedetention =  models.ForeignKey(Duree, related_name='duree_detention', on_delete=models.DO_NOTHING, verbose_name="Jours, mois, ans etc?", null=True, blank=True)
    probationON = models.BooleanField(verbose_name="Probation? Cocher si oui")
    probationduree = models.CharField(max_length=50, verbose_name="Durée de la probation", null=True, blank=True)
    uniteprobation =  models.ForeignKey(Duree, related_name='duree_probation', on_delete=models.DO_NOTHING, verbose_name="Jours, mois, ans etc?", null=True, blank=True)
    interdictionON = models.BooleanField(verbose_name="Interdiction? Cocher si oui")
    interdictionduree = models.CharField(max_length=50, verbose_name="Durée de l'interdiction", null=True, blank=True)
    uniteinterdiction =  models.ForeignKey(Duree, related_name='duree_interdiction', on_delete=models.DO_NOTHING, verbose_name="Jours, mois, ans etc?", null=True, blank=True)
    interdictiondetails = models.CharField(max_length=150, verbose_name="Détails à propos de l'interdicttion", null=True, blank=True)
    surcisON = models.BooleanField(verbose_name="Surcis? Cocher si oui")
    surcisduree = models.CharField(max_length=50, verbose_name="Durée du surcis", null=True, blank=True)
    unitesurcis =  models.ForeignKey(Duree, related_name='duree_surcis', on_delete=models.DO_NOTHING, verbose_name="Jours, mois, ans etc?", null=True, blank=True)
    autreON = models.BooleanField(verbose_name="Autre? Cocher si oui")
    autredetails = models.CharField(max_length=100, blank=True, null=True,verbose_name="Si autre : détails")
    consecutifsON = models.BooleanField(default=0,verbose_name="Consécutif? Cocher si oui")
    RA = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    card = models.IntegerField(default=1)
    nouveaudelit = models.BooleanField()

    class Meta:
        ordering = ['personnegrc', 'date_sentence', 'ordre_delit']
        unique_together = (('personnegrc', 'date_sentence', 'ordre_delit','RA'),)
        indexes = [models.Index(fields=['personnegrc', 'date_sentence', 'ordre_delit','RA'])]

    def __str__(self):
        return '%s %s %s' % (self.personnegrc, self.date_sentence, self.ordre_delit)


# Une fiche pour chaque liberation de chaque personne.
class Liberationntp1(models.Model):
    personnegrc = models.ForeignKey(Personnegrcntp1, on_delete=models.CASCADE, verbose_name="ID")
    date_liberation = models.DateField(verbose_name="Date de la libération (jj/mm/aaaa)")
    type = models.BooleanField(verbose_name="Libération absolue? Cocher si oui")
    RA = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['personnegrc', 'date_liberation']

    def __str__(self):
        return '%s %s' % (self.personnegrc, self.date_liberation)