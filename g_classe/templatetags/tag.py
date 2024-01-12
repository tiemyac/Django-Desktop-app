from django import template
from g_classe.views import cookie
from g_classe.models import *


register = template.Library()


@register.simple_tag
def notation(coefficient):
    return coefficient * 10

@register.simple_tag
def calcul_total(items):
    try:
        res = [item['note'] for item in items]
    except:
        res = [item.note for item in items]
    return sum(res)


@register.simple_tag
def calcul_moyenne(items):
    try:
        total = sum([item['note'] for item in items])
    except:
        total = sum([item.note for item in items])
    coeff = calcul_coefficient(items)
    moyenne = total / coeff
    return round(moyenne,2)


@register.simple_tag
def appreciation(items):
    moyenne = calcul_moyenne(items)
    app = "Erreur d'appreciation"
    if moyenne >= 7:
        app = "Excellent travail"
    elif moyenne >= 5 < 7:
        app = "Travail moyen"
    else:
        app = "Travail faible"
    return app


@register.simple_tag
def config_url(url):
    return url[1:]


@register.simple_tag
def calcul_coefficient(items):
    try:
        coeff = sum([item['matiere'].coefficient for item in items])
    except:
        coeff = sum([item.matiere.coefficient for item in items])
    return coeff

@register.simple_tag
def objectif_points(items):
    coeff = calcul_coefficient(items)
    return coeff * 10


@register.simple_tag
def get_rang(studient, trimestre):
    list = []
    studients = StudientOfYear.objects.filter(annee_scolaire=cookie.pk)
    for std in studients:
        note = std.notes.filter(studient=std, trimestre=trimestre.pk)
        if not note:
            total = 0
        else:
            for item in note:
                total = calcul_total(item.note.all())
        list.append({'studient': std.studient, 'total': total})
    result = add_position_to_list(list)
    rang = find_rang(result, studient)
    return {'rang' : rang['rang'], 'indice': get_indice_rang(studient, rang['rang']), 'effectif': len(studients)}


def add_position_to_list(tab):
    # Trier la liste en fonction de la clé 'total'
    sorted_tab = sorted(tab, key=lambda x: x['total'], reverse=True)

    # Ajouter la clé 'position' basée sur l'index après le tri
    for i, item in enumerate(sorted_tab):
        item['rang'] = i + 1

    return sorted_tab


def find_rang(list, studient):
    for item in list:
        if item['studient'].pk == studient.pk:
            result = item
            break
    return result


def get_indice_rang(studient, rang):
    if rang == 1:
        if studient.sexe == "F":
            indice = "ère"
        else:
            indice = "er"
    else:
        indice = "ème"
    return indice

