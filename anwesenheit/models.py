from django.db import models

class Anwesenheit(models.Model):
    person = models.ForeignKey('Schueler', on_delete=models.CASCADE)
    datum = models.DateField()
    uhrzeit = models.TimeField()
    anwesend = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.person} am {self.datum} um {self.uhrzeit}'

class RFIDChip(models.Model):
    person = models.OneToOneField('Schueler', on_delete=models.CASCADE)
    chip_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.chip_id} für {self.person}'

class Wohnort(models.Model):
    plz = models.CharField(max_length=6)
    stadt = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.plz} {self.stadt}'

class Strasse(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Kontaktdaten(models.Model):                        
    wohnort = models.ForeignKey(Wohnort, on_delete=models.PROTECT)
    strasse = models.ForeignKey(Strasse, on_delete=models.PROTECT)
    hausnummer = models.CharField(max_length=6)
    telefonnummer = models.CharField(max_length=20)
    email = models.EmailField(max_length=254, unique=True)

    def __str__(self):
        return f'{self.strasse} {self.hausnummer}, {self.wohnort}, Tel: {self.telefonnummer}'


class Person(models.Model):
    vorname = models.CharField(max_length=50)       
    nachname = models.CharField(max_length=50)
    anwesend = models.BooleanField(default=False)   
    kontaktdaten = models.ForeignKey(Kontaktdaten, on_delete=models.PROTECT)
    geburtstag = models.DateField('Geburtstagsdatum')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  

    def __str__(self):
        return f'{self.vorname} {self.nachname} {self.anwesend} {self.kontaktdaten}'

class Klasse(models.Model):
    bezeichnung = models.CharField(max_length=20)
    jahrgang = models.PositiveIntegerField()
    lehrer = models.ForeignKey('Lehrer', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('bezeichnung', 'jahrgang')   # Kombination eindeutig

    def __str__(self):
        return f'{self.bezeichnung} ({self.jahrgang})'

class Schueler(Person):
    klasse = models.ForeignKey(Klasse, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Schüler"
        verbose_name_plural = "Schüler"

class Lehrer(Person):
    fach = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.vorname} {self.nachname}'  