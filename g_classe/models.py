from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import datetime


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year()+1)(value)


class Classe(models.Model):
    classe = models.CharField(max_length=60)
    dimunitif = models.CharField(max_length=10)
    cours = models.IntegerField()

    def __str__(self):
        return f'{self.classe} ({self.dimunitif})'


class Annee_Scolaire(models.Model):
    annee_scolaire = models.CharField(max_length=30, null=True, blank=True)
    start = models.IntegerField(('year'), validators=[MinValueValidator(2020), max_value_current_year], null=True, blank=True)
    end = models.IntegerField(('year'), validators=[MinValueValidator(2020), max_value_current_year], null=True, blank=True)

    status = models.CharField(max_length=10, choices=(('Actif', 'Actif'), ('#', '#')), default="#", null=True, blank=True)
    ecole = models.CharField(max_length=255, null=True, blank=True)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.annee_scolaire = f'{self.start} - {self.end}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.annee_scolaire
    

class Trimestre(models.Model):
    annee_scolaire = models.ForeignKey(Annee_Scolaire, on_delete=models.CASCADE)
    trimestre = models.CharField(max_length=60)

    def __str__(self):
        return self.trimestre


class Matiere(models.Model):
    matiere = models.CharField(max_length=25)
    coefficient = models.IntegerField()
    cours = models.IntegerField()

    def __str__(self):
        return self.matiere


class Studient(models.Model):
    GENRE = (('M', 'Masculin'), ('F', 'Féminin'))
    nom = models.CharField(max_length=60)
    prenom = models.CharField(max_length=60)
    sexe = models.CharField(max_length=10, choices=GENRE)
    naissance = models.DateField()

    def __str__(self):
        return f'{self.nom} {self.prenom}'


class StudientOfYear(models.Model):
    STATUS = (('PRE', 'Présent(e)'), ('ABS', 'Absent(e)'), ('ABA', 'Abandon'))
    annee_scolaire = models.ForeignKey(Annee_Scolaire, on_delete=models.CASCADE)
    studient = models.ForeignKey(Studient, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS, default='PRE')

    def __str__(self):
        return f'{self.studient.nom} {self.studient.prenom}'


class Note(models.Model):
    studient = models.ForeignKey(StudientOfYear, on_delete=models.CASCADE, related_name='notes')
    trimestre = models.ForeignKey(Trimestre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.studient.studient.nom} {self.studient.studient.prenom}'


class Notes(models.Model):
    keyNote = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='note')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    note = models.IntegerField()
    def __str__(self):
        return self.matiere.matiere
