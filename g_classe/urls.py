# pages/urls.py
from django.urls import path
from g_classe.views import *

urlpatterns = [
    path('', homePageView, name='home'),
    path('note', notes, name='note'),
    path('synoptique', synoptique, name='synoptique'),
    path('get_synoptique', get_synoptique, name='get_synoptique'),
    path('edit_note', add_note, name='edit_note'),
    path('drag_studient', drag_studient, name='drag_studient'),
    path('old_studient', old_studient, name='old_studient'),
    path('on_drag_studient', on_drag_studient, name='on_drag_studient'),
    path('view_note/<int:pk>/', view_note_by_studient, name='view_note'),
    path('edit_studient/<int:pk>/', edit_studient, name='edit_studient'),
    path('change_studient_status/<int:pk>/<str:status>/', change_studient_status, name='change_studient_status'),
    path('change_year/<int:year_select>)', change_year, name='change_year'),

    path('guide', documentation, name="guide"),
    path('propos', propos, name="propos"),

    path('setting', set_setting, name="setting"),
    path('studient', studient, name='studient')
]
