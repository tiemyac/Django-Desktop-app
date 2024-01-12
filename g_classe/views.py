# pages/views.py
from django.db.models import Q, F, Max, OuterRef, Exists
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from g_classe.forms import *
from g_classe.models import *
from django.forms.formsets import formset_factory
from django.contrib import messages
from django.db.models import Subquery



cookie = Annee_Scolaire.objects.get(status="Actif")
context = {
        'ecole': cookie.ecole,
        'classe': cookie.classe.classe,
        'annee_scolaire': cookie.annee_scolaire,
        'page': '',
        'title': '',
        'years': Annee_Scolaire.objects.filter(status="#")
    }


def homePageView(request):
    context['page'] = ""
    context['title'] = ""
    context['classe'] = ""
    return render(request, 'pages/index.html', context)


def notes(request):
    context['title'] = 'Liste des notes'
    items = StudientOfYear.objects.filter(annee_scolaire=cookie)
    fields = []
    response = []
    for item in items:
        for k in item.notes.all():
            response.append({'studient': item.studient, 'trimestre': k.trimestre,
                             'notes': k.note.all()})
            fields = k.note.all()

    context['items'] = response
    context['fields'] = fields
    return render(request, 'pages/notes.html', context)


def add_note(request):
    MATIERES = [{'matiere': (item.pk, item.matiere), 'note': item.matiere} for item in
                Matiere.objects.filter(cours=cookie.classe.cours)]
    context['page'] = "Notes"
    context['title'] = "Ajout de notes"
    formset = formset_factory(NoteForm, extra=0)
    form = formset(initial=MATIERES)
    context['studients'] = StudientOfYear.objects.filter(annee_scolaire=cookie)
    context['trimestres'] = Trimestre.objects.filter(annee_scolaire=cookie)

    if request.method == 'POST':
        studient = request.POST['studient_id']
        trimestre = request.POST['trimestre_id']
        if studient != '':
            ins_studient = StudientOfYear.objects.get(studient=studient, annee_scolaire=cookie.pk)
            ins_trimestre = Trimestre.objects.get(pk=trimestre)
            forms = formset(request.POST)
            try:
                note = Note.objects.get(studient=ins_studient,trimestre=ins_trimestre)
                for f in forms:
                    if f.is_valid():
                        matr = f.cleaned_data['matiere']
                        nt = f.cleaned_data['note']
                        instance = Notes.objects.get(keyNote=note, matiere=matr)
                        instance.note = nt
                        instance.save()
                    messages.success(request, 'Note enregistrée avec succès')
            except Exception as ex:
                n = Note(studient=ins_studient, trimestre=ins_trimestre)
                n.save()
                note = Note.objects.get(studient=ins_studient, trimestre=ins_trimestre)
                for f in forms:
                    obj = f.save(commit=False)
                    obj.keyNote = note
                    obj.save()
                    messages.success(request, 'Note enregistrée avec succès')

    context['form'] = form
    return render(request, 'pages/add_note.html', context)


def view_note_by_studient(request, pk):
    params = pk
    response = []
    try:
        studient = StudientOfYear.objects.get(annee_scolaire=cookie.pk, studient=params)
        notes = Note.objects.filter(studient=studient)
        context['studient'] = studient
        for i in notes:
            results = [{'matiere': item.matiere, 'note': item.note} for item in i.note.all()]
            response.append({'trimestre': i.trimestre, 'notes': results})
        #return JsonResponse(response, safe=False)
        context['items'] = response
    except Exception as ex:
        context['items'] = response
        #return JsonResponse([{"error": "Elève inexistant"}], safe=False)

    return render(request, 'pages/detail_note.html', context)


def get_synoptique(request):
    param = request.GET
    if param['trimestre'] == '':
        trimestre = Trimestre.objects.filter(annee_scolaire=cookie.pk).first()
    else:
        trimestre = Trimestre.objects.get(pk=param['trimestre'])

    try:
        trimestre = Trimestre.objects.get(pk=trimestre.pk)
        notes = Note.objects.filter(trimestre=trimestre.pk)
        data = [{'sexe': item.studient.studient.sexe, 'notes': item.note.all()} for item in notes]
        res = setPrevalence(data)
        return JsonResponse({"data1": res['moyennes'], "data2": res['p_moyennes'], "columns_m": list(res['moyennes'][0].keys()), "columns_p": list(res['p_moyennes'][0].keys())}, safe=False)
    except Exception as ex:
        return JsonResponse({'error': 'Echec'}, safe=False)


def synoptique(request):
    context['title'] = "Tableau synoptique"
    context["columns"] = Matiere.objects.filter(cours=cookie.classe.cours)
    context['trimestres'] = Trimestre.objects.filter(annee_scolaire=cookie.pk)

    return render(request, 'pages/synoptique.html', context)


def setPrevalence(items):
    data1 = []
    data2 = []
    columns = Matiere.objects.filter(cours=cookie.classe.cours)
    for column in columns:
        moyennes = {}
        p_moyennes = {}
        m_m = 0
        m_f = 0
        p_m = 0
        p_f = 0
        for item in items:
            for obj in item['notes']:
                if obj.matiere == column:
                    if obj.note >= (obj.matiere.coefficient * 10) / 2:
                        if item['sexe'] == 'M':
                            m_m = m_m + 1
                        else:
                            m_f = m_f + 1
                    else:
                        if item['sexe'] == 'M':
                            p_m = p_m + 1
                        else:
                            p_f = p_f + 1
                    break
        moyennes['m_m'] = m_m
        moyennes['m_f'] = m_f
        p_moyennes['p_m'] = p_m
        p_moyennes['p_f'] = p_f
        data1.append(moyennes)
        data2.append(p_moyennes)
    results = {'moyennes': data1, 'p_moyennes': data2}
    """              
    for item in items:

        for column in columns:
            matieres = {}

            matieres["matiere"] = {'name': column.matiere, "moyenne": 0}
            for obj in item['notes']:
                m_m = 0
                m_f = 0
                p_m = 0
                p_f = 0
                if obj.matiere == column:
                    if obj.note >= (obj.matiere.coefficient * 10) / 2:
                        if item['sexe'] == 'M':
                            m_m = m_m + 1
                        else:
                            m_f = m_f + 1
                    else:
                        if item['sexe'] == 'M':
                            p_m = p_m + 1
                        else:
                            p_f = p_f + 1
                    break
                matieres['matiere']['moyenne'] = m_m
            results.append(matieres)
        print(results)
    """
    return results


def change_year(request,year_select):
    global cookie

    try:
        new_default = Annee_Scolaire.objects.get(pk=year_select)
        default = Annee_Scolaire.objects.get(pk=cookie.pk)
        default.status = "#"
        default.save()
        new_default.status = "Actif"
        new_default.save()
        cookie = new_default

        global context
        context = {
            'ecole': cookie.ecole,
            'classe': cookie.classe.dimunitif,
            'annee_scolaire': cookie.annee_scolaire,
            'page': '',
            'title': '',
            'years': Annee_Scolaire.objects.filter(status="#")
        }
        messages.info(request, "Vous avez changé l'année scolaire en cours")
        return redirect("/")
    except Exception as ex:
        return redirect("/")



def set_setting(request):
    form = SettingForm()

    if request.method == 'POST':
        form = SettingForm(request.POST)
        if form.is_valid():
            obj = form.save()
            obj1 = Trimestre(annee_scolaire=obj, trimestre="Premier trimestre")
            obj2 = Trimestre(annee_scolaire=obj, trimestre="Deuxième trimestre")
            obj3 = Trimestre(annee_scolaire=obj, trimestre="Troisième trimestre")
            obj1.save()
            obj2.save()
            obj3.save()
        global context
        context = {
            'ecole': cookie.ecole,
            'classe': cookie.classe.dimunitif,
            'annee_scolaire': cookie.annee_scolaire,
            'page': '',
            'title': '',
            'years': Annee_Scolaire.objects.filter(status="#")
        }
    context['form'] = form
    context['items'] = Annee_Scolaire.objects.all()
    return render(request, 'settings/index.html', context)


def studient(request):
    context['page'] = 'Elèves'
    context['title'] = 'Gestion des élèves'
    if request.method == 'POST':
        form = StudientForm(request.POST)
        if form.is_valid():
            obj = form.save()
            el = StudientOfYear(annee_scolaire=cookie, studient=obj)
            el.save()
            messages.success(request, 'Nouveau élève enregistré avec succès')

    studients = StudientOfYear.objects.filter(annee_scolaire=cookie.pk).order_by('status')
    context['items'] = studients
    context['ABS'] = len(studients.filter(annee_scolaire=cookie.pk, status='ABS'))
    context['ABA'] = len(studients.filter(annee_scolaire=cookie.pk, status='ABA'))
    context['PRE'] = len(studients.filter(annee_scolaire=cookie.pk, status='PRE'))
    context['form'] = StudientForm()

    return render(request, 'pages/studients.html', context)


def drag_studient(request):
    studients = StudientOfYear.objects.filter(annee_scolaire=cookie.pk)
    context['studients'] = studients
    years = Annee_Scolaire.objects.filter(~Q(pk=cookie.pk))
    context["i_years"] = years
    return render(request, 'pages/drag_studients.html', context)


def old_studient(request):
    param = request.GET
    try:
        if param['year'] == '':
            # Récupérer les identifiants des étudiants pour une année scolaire spécifique
            year_studients_ids = StudientOfYear.objects.filter(annee_scolaire=cookie.pk).values_list('studient',
                                                                                                     flat=True)
            # Filtrer tous les étudiants excluant ceux de l'année scolaire spécifique
            old_studients = StudientOfYear.objects.exclude(studient__in=Subquery(year_studients_ids))
            studients = remove_duplicates(old_studients,'studient')
        else:
            year_studients_ids = StudientOfYear.objects.filter(annee_scolaire=cookie.pk).values_list('studient',
                                                                                                     flat=True)
            studients = StudientOfYear.objects.filter(annee_scolaire=param['year']).exclude(studient__in=Subquery(year_studients_ids))

        res = [{'id': item.pk, 'name': f'{item.studient.nom} {item.studient.prenom}', 'naissance': item.studient.naissance, 'sexe': item.studient.sexe} for item in studients]
        return JsonResponse(res, safe=False)
    except Exception as ex:
        return JsonResponse({'error': 'Echec'}, safe=False)


def on_drag_studient(request):
    param = request.POST
    try:
        studient = StudientOfYear.objects.get(pk=param['studient'])
        new_year_studient = StudientOfYear(studient=studient.studient)
        new_year_studient.annee_scolaire = cookie
        new_year_studient.save()
        #print(studient.studient)
    except:
        print('erreur')
        pass
    return HttpResponse()


def remove_duplicates(objects_list, key):
    seen = set()
    unique_objects = []

    for obj in objects_list:
        obj_key = obj.studient
        if obj_key not in seen:
            seen.add(obj_key)
            unique_objects.append(obj)

    return unique_objects


def edit_studient(request, pk):
    object = Studient.objects.get(pk=pk)
    form = StudientForm(instance=object)
    if request.method == 'POST':
        form = StudientForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            messages.success(request, 'Modification apportée avec succès', 'success')
    context['form'] = form
    context['title'] = 'Modification de données'
    return render(request, 'pages/edit_studient.html', context)


def change_studient_status(request, pk, status):
    try:
        item = StudientOfYear.objects.get(pk=pk)
        item.status = status
        item.save()
        messages.success(request, f'{item.prenom} est consideré(e) comme * {status} *', 'success')
        return redirect('studient')
    except:
        messages.error(request, 'Echec de modifiaction!!')
        return redirect('studient')


def propos(request):

    return render(request, 'pages/propos.html', context)


def documentation(request):

    return render(request, 'pages/documentation.html', context)




