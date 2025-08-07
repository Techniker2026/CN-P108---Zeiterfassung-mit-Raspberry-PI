from django.contrib import admin                    # Modelle im Django-Admin sichtbar machen
from django import forms                            # eigene Eingabeformulare definieren
from .models import Anwesenheit, Schueler, Lehrer   # eigene Modelle importieren
from django.contrib.contenttypes.models import ContentType

# eigenes Formular für Admin, dass auf Modell Anwesenheit basiert
class AnwesenheitForm(forms.ModelForm):             # neue Klasse, Django-Formular automatische Felder
    schueler = forms.ModelChoiceField(queryset=Schueler.objects.all(), required=False)  # Dropdownmenü mit Schüler, nicht zwingend erforderlich
    lehrer = forms.ModelChoiceField(queryset=Lehrer.objects.all(), required=False)      # Dropdownmenü mit Lehrer, nicht zwingend erforderlich

    class Meta:                                         # Metaklasse
        model = Anwesenheit                             # Formular basiert auf der Anwesenheitsklasse
        fields = ['datum', 'uhrzeit', 'anwesend', 'schueler', 'lehrer']     # Daten die angezeigt werden sollen

    def speichern(self, speichern_direkt=True):
        # Erzeugt eine Instanz, speichert aber noch nicht in die Datenbank
        instanz = super().save(commit=False)

        # Holt die Eingaben aus dem Formular
        schueler = self.cleaned_data.get('schueler')
        lehrer = self.cleaned_data.get('lehrer')

        # Prüft, ob beide oder keiner ausgewählt wurden
        if schueler and lehrer:
            raise ValidationError("Bitte wähle **entweder** einen Schüler **oder** einen Lehrer – nicht beides.")
        elif schueler:
            # Setze ContentType und object_id für generische Beziehung auf Schüler
            instanz.content_type = ContentType.objects.get_for_model(Schueler)
            instanz.object_id = schueler.id
        elif lehrer:
            # Setze ContentType und object_id für generische Beziehung auf Lehrer
            instanz.content_type = ContentType.objects.get_for_model(Lehrer)
            instanz.object_id = lehrer.id
        else:
            raise ValidationError("Bitte wähle einen Schüler **oder** einen Lehrer aus.")

        # Wenn direkt gespeichert werden soll:
        if speichern_direkt:
            instanz.save()

        return instanz

class AnwesenheitAdmin(admin.ModelAdmin):
    form = AnwesenheitForm  # das eigene Formular aktivieren
    list_display = ('get_person_name', 'datum', 'uhrzeit', 'anwesend')
    list_filter = ('datum', 'anwesend')
    search_fields = ('object_id',)

    def get_person_name(self, obj):
        return str(obj.person)
    get_person_name.short_description = 'Person'