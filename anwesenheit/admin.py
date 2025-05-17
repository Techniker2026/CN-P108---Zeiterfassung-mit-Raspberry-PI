from django.contrib import admin                    # Modelle im Django-Admin sichtbar machen
from django import forms                            # eigene Eingabeformulare definieren
from .models import Anwesenheit, Schueler, Lehrer   # eigene Modelle importieren
from django.contrib.contenttypes.models import ContentType

# eigenes Formular für Admin, dass auf Modell Anwesenheit basiert
class AnwesenheitForm(forms.ModelForm):             # neue Klasse, Django-Formular automatische Felder
    schueler = forms.ModelChoiceField(queryset=Schueler.objects.all(),)required=False)  # Dropdownmenü mit Schüler, nicht zwingend erforderlich
    lehrer = forms.ModelChoiceField(queryset=Lehrer.objects.all(), required=False)      # Dropdownmenü mit Lehrer, nicht zwingend erforderlich

class Meta:
    model = Anwesenheit
    fields = ['datum', 'uhrzeit', 'anwesend', 'schueler', 'lehrer']
