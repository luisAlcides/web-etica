from django import forms
from .models import Tema

class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ['titulo', 'contenido']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'border p-2 w-full'}),
            'contenido': forms.Textarea(attrs={'class': 'border p-2 w-full'}),
        }
