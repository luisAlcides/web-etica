from django import forms
from .models import Tema, Pregunta, Opcion

class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ['titulo', 'contenido']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'border p-2 w-full'}),
            'contenido': forms.Textarea(attrs={'class': 'border p-2 w-full'}),
        }



class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['tema', 'texto']
        widgets = {
            'tema': forms.Select(attrs={'class': 'w-full border border-gray-300 p-2 rounded'}),
            'texto': forms.Textarea(attrs={'class': 'w-full border border-gray-300 p-2 rounded', 'rows': 3}),
        }

class OpcionForm(forms.ModelForm):
    class Meta:
        model = Opcion
        fields = ['texto', 'es_correcta']
        widgets = {
            'texto': forms.TextInput(attrs={'class': 'w-full border border-gray-300 p-2 rounded'}),
            'es_correcta': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600'}),
        }