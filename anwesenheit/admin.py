from django.contrib import admin
from .models import Anwesenheit

@admin.register(Anwesenheit)
class AnwesenheitAdmin(admin.ModelAdmin):
    list_display = ('person', 'datum', 'uhrzeit', 'anwesend')
    list_filter = ('datum', 'anwesend')
    search_fields = ('object_id',)

from .models import Schueler, Lehrer

admin.site.register(Schueler)
admin.site.register(Lehrer)
