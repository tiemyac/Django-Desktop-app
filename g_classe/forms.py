from django import forms
from g_classe.models import *
import datetime

#TRIMESTRE = [(item.pk, item.trimestre) for item in Trimestre.objects.filter(annee_scolaire=cookie)]
#MATIERES = [{'matiere':(item.pk, item.matiere)} for item in Matiere.objects.filter(cours=cookie.classe.cours)]


def year_choices():
    return [(r,r) for r in range(2020, datetime.date.today().year + 2)]


class SettingForm(forms.ModelForm):
    start = forms.TypedChoiceField(coerce=int, choices=year_choices,
                                   initial=current_year, label='An 1',
                                   widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'yyyy'}))
    end = forms.TypedChoiceField(coerce=int, choices=year_choices,
                                 initial=current_year, label='An 2',
                                 widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'yyyy'}))
    ecole = forms.CharField(label='Ecole', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nom de l\'école'
    }))

    class Meta:
        model = Annee_Scolaire
        fields = ['start', 'end', 'ecole', 'classe']
        widgets = {
            'classe': forms.Select(attrs={'class': 'form-control', })
        }


class MatiereForm(forms.ModelForm):
    matiere = forms.CharField(label='Matière', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Matière'
    }))
    coefficient = forms.IntegerField(label='Coefficient', widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Coefficient de la matière'
    }))
    class Meta:
        model = Matiere
        fields = ['matiere', 'coefficient']


class StudientForm(forms.ModelForm):
    nom = forms.CharField(label='NOM', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nom de l\'élève'
    }))
    prenom = forms.CharField(label='PRENOM(S)', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Prenom(s) de l\'élève'
    }))

    naissance = forms.DateField(label='DATE DE NAISSANCE', widget=forms.DateInput(attrs={
        'class': 'form-control',
        'placeholder': 'Date de naissance',
        'type': 'date'
    }))
    class Meta:
        model = Studient
        fields = ['nom', 'prenom', 'sexe', 'naissance']
        labels = {'sexe': 'GENRE'}
        widgets = {
            'sexe': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Genre'})
        }


class NoteForm(forms.ModelForm):
    """
    trimestre = forms.TypedChoiceField(choices=TRIMESTRE,
                                 widget=forms.Select(attrs={'class': 'form-control', 'placeholder': '----'}))

    matiere = forms.TypedChoiceField(choices=MATIERES,
                                       widget=forms.Select(attrs={'class': 'form-control', 'placeholder': '----'}))
    """
    note = forms.IntegerField(label='Note', widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Note de la matière'
    }))
    class Meta:
        model = Notes
        fields = ('matiere', 'note')
        widgets = {
            'matiere': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Matiere',
            }),
        }



