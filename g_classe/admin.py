from django.contrib import admin
from g_classe.models import *
# Register your models here.

class ClasseAdmin(admin.ModelAdmin):
    list_display = ('classe', 'dimunitif', 'cours')

class MatiereAdmin(admin.ModelAdmin):
    list_display = ('matiere', 'coefficient', 'cours')

class Annee_ScolaireAdmin(admin.ModelAdmin):
    list_display = ('annee_scolaire', 'start', 'end', 'ecole', 'classe', 'status')

class StudientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'sexe', 'naissance')

class StudientOfYearAdmin(admin.ModelAdmin):
    list_display = ('annee_scolaire', 'studient', 'status')


class NoteAdmin(admin.ModelAdmin):
    list_display = ('studient', 'trimestre')

class NotesAdmin(admin.ModelAdmin):
    list_display = ('keyNote', 'matiere', 'note')


admin.site.register(Classe,ClasseAdmin)
admin.site.register(Annee_Scolaire, Annee_ScolaireAdmin)
admin.site.register(Matiere,MatiereAdmin)
admin.site.register(Trimestre)
admin.site.register(Studient, StudientAdmin)
admin.site.register(StudientOfYear, StudientOfYearAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Notes, NotesAdmin)

