from django.contrib import admin
from .models import Schueler

@admin.register(Schueler)
class SchuelerAdmin(admin.ModelAdmin):
    list_display = ('vorname', 'nachname', 'anwesend')     # zeigt Felder in der Übersicht
    list_filter = ('anwesend',)             # fügt Filteroption hinzu
    search_fields = ('name',)               # ermöglicht Suche