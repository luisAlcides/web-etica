from django.contrib import admin
from .models import Tema, Pregunta, Opcion, Resultado

class OpcionInline(admin.TabularInline):
    model = Opcion
    extra = 4

class PreguntaAdmin(admin.ModelAdmin):
    list_display = ['texto', 'tema']
    inlines = [OpcionInline]

admin.site.register(Tema)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(Resultado)
