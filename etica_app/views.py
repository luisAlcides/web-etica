from django.shortcuts import render, get_object_or_404, redirect
from .models import Contenido, Ejercicio, Tema
from .forms import TemaForm
from django.contrib.auth.decorators import login_required, user_passes_test


def index(request):
    contenidos = Contenido.objects.all()
    return render(request, 'etica_app/index.html', {'contenidos': contenidos})

def detalle_contenido(request, contenido_id):
    contenido = Contenido.objects.get(id=contenido_id)
    return render(request, 'etica_app/detalle_contenido.html', {'contenido': contenido})

def lista_ejercicios(request):
    ejercicios = Ejercicio.objects.all()
    if request.method == 'POST':
        respuestas = []
        for ejercicio in ejercicios:
            respuesta_usuario = request.POST.get(str(ejercicio.id))
            correcta = respuesta_usuario.strip().lower() == ejercicio.respuesta_correcta.strip().lower()
            respuestas.append((ejercicio, respuesta_usuario, correcta))
        return render(request, 'etica_app/resultados.html', {'respuestas': respuestas})
    return render(request, 'etica_app/ejercicios.html', {'ejercicios': ejercicios})

def es_admin(user):
    return user.is_staff


def lista_temas(request):
    temas = Tema.objects.all()
    return render(request, 'etica_app/lista_temas.html', {'temas': temas})

def detalle_tema(request, tema_id):
    tema = get_object_or_404(Tema, id=tema_id)
    return render(request, 'etica_app/detalle_tema.html', {'tema': tema})

@login_required
@user_passes_test(es_admin)
def crear_tema(request):
    if request.method == 'POST':
        form = TemaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_temas')
    else:
        form = TemaForm()
    return render(request, 'etica_app/crear_tema.html', {'form': form})

@login_required
@user_passes_test(es_admin)
def editar_tema(request, tema_id):
    tema = get_object_or_404(Tema, id=tema_id)
    if request.method == 'POST':
        form = TemaForm(request.POST, instance=tema)
        if form.is_valid():
            form.save()
            return redirect('detalle_tema', tema_id=tema.id)
    else:
        form = TemaForm(instance=tema)
    return render(request, 'etica_app/editar_tema.html', {'form': form, 'tema': tema})

@login_required
@user_passes_test(es_admin)
def eliminar_tema(request, tema_id):
    tema = get_object_or_404(Tema, id=tema_id)
    if request.method == 'POST':
        tema.delete()
        return redirect('lista_temas')
    return render(request, 'etica_app/eliminar_tema.html', {'tema': tema})
