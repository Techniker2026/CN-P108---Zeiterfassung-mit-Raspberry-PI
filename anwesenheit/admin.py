from django.contrib import admin                    # Modelle im Django-Admin sichtbar machen
from django import forms                            # eigene Eingabeformulare definieren
from .models import Anwesenheit, Schueler, Lehrer   # eigene Modelle importieren
from django.contrib.contenttypes.models import ContentType

# eigenes Formular für Admin, dass auf Modell Anwesenheit basiert
class AnwesenheitForm(forms.ModelForm):             # neue Klasse, Django-Formular automatische Felder
    schueler = forms.ModelChoiceField(queryset=Schueler.objects.all(),)required=False)  # Dropdownmenü mit Schüler, nicht zwingend erforderlich
    lehrer = forms.ModelChoiceField(queryset=Lehrer.objects.all(), required=False)      # Dropdownmenü mit Lehrer, nicht zwingend erforderlich

    class Meta:                                         # Metaklasse
        model = Anwesenheit                             # Formular basiert auf der Anwesenheitsklasse
        fields = ['datum', 'uhrzeit', 'anwesend', 'schueler', 'lehrer']     # Daten die angezeigt werden sollen

    def speichern(self, speichern_direkt=True):     # self, akkutelle Instanz des Objekt, commit=True -> speichert das Objekt sofort
        instanz = super().save(commit=False)        # super() ist python funktion die Methoden aus Eltrnklasse aufruft, save ruft Methode der Elternklasse (ModelForm) auf, commmit=false speichert es noch nicht 
        if self.cleaned_data['schueler']:           # self.cleaned_data ist ein dictionary(von django) mit allen formular daten, wurde im feld schueler schon etwas ausgewählt
            instanz.content_type = ContentType.objects.get_for_model(Schueler)
            instanz.object_id = self.cleaned_data['schueler'].id
        elif self.cleaned_data['lehrer']:
            instanz.content_type = ContentType.objects.get_for_model(Lehrer)
            instanz.object_id = self.cleaned_data['lehrer'].id
        if speichern_direkt:
            instanz.save()
        return instanz
