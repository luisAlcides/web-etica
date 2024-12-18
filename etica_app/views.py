from django.shortcuts import render, get_object_or_404, redirect
from .models import Tema, Pregunta, Opcion, Resultado, Contenido, Ejercicio
from .forms import TemaForm, PreguntaForm, OpcionForm
from django.contrib.auth.decorators import login_required, user_passes_test
import markdown
from django import template
from django.utils.safestring import mark_safe
from django.db.models import Q
import bleach
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.utils import timezone



def index(request):
    contenidos = Contenido.objects.all()
    return render(request, 'etica_app/index.html', {'contenidos': contenidos})

def bibliografia(request):
    return render(request, 'etica_app/bibliografia.html')

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

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    html = markdown.markdown(text, extensions=['extra', 'codehilite'])
    # Configurar las etiquetas y atributos permitidos
    allowed_tags = bleach.sanitizer.ALLOWED_TAGS + [
        'p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'img', 'hr', 'br', 'pre', 'code', 'blockquote', 'ul', 'ol', 'li',
        'table', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td', 'em', 'strong',
    ]
    allowed_attributes = bleach.sanitizer.ALLOWED_ATTRIBUTES
    allowed_attributes.update({
        '*': ['class', 'style'],
        'a': ['href', 'title'],
        'img': ['src', 'alt', 'title'],
    })
    cleaned_html = bleach.clean(html, tags=allowed_tags, attributes=allowed_attributes)
    return mark_safe(cleaned_html)

def buscar_temas(request):
    query = request.GET.get('q', '')
    resultados = []
    if query:
        resultados = Tema.objects.filter(
            Q(titulo__icontains=query) |
            Q(contenido__icontains=query)
        ).distinct()
    return render(request, 'etica_app/buscar_temas.html', {'resultados': resultados, 'query': query})


def lista_temas_ejercicios(request):
    temas = Tema.objects.filter(preguntas__isnull=False).distinct()
    return render(request, 'etica_app/lista_temas_ejercicios.html', {'temas': temas})


def realizar_examen(request, tema_id):
    tema = get_object_or_404(Tema, id=tema_id)
    preguntas = tema.preguntas.all()

    if request.method == 'POST':
        puntaje = 0
        total_preguntas = preguntas.count()

        for pregunta in preguntas:
            opcion_id = request.POST.get(str(pregunta.id))
            if opcion_id:
                opcion_seleccionada = Opcion.objects.get(id=opcion_id)
                if opcion_seleccionada.es_correcta:
                    puntaje += 1

        porcentaje = int((puntaje / total_preguntas) * 100)

        # Guardar el resultado
        Resultado.objects.create(usuario=request.user, tema=tema, puntaje=porcentaje)
        return render(request, 'etica_app/resultado_examen.html', {
            'tema': tema,
            'puntaje': puntaje,
            'total_preguntas': total_preguntas,
            'porcentaje': porcentaje,
        })

    else:
        return render(request, 'etica_app/realizar_examen.html', {'tema': tema, 'preguntas': preguntas})

def lista_preguntas(request):
    preguntas = Pregunta.objects.all()
    return render(request, 'etica_app/lista_preguntas.html', {'preguntas': preguntas})


def ver_resultados(request):
    resultados = Resultado.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'etica_app/ver_resultados.html', {'resultados': resultados})

@user_passes_test(es_admin)
def crear_pregunta(request):
    OpcionFormSet = inlineformset_factory(Pregunta, Opcion, form=OpcionForm, extra=4, can_delete=False)
    if request.method == 'POST':
        pregunta_form = PreguntaForm(request.POST)
        formset = OpcionFormSet(request.POST)
        if pregunta_form.is_valid() and formset.is_valid():
            pregunta = pregunta_form.save()
            opciones = formset.save(commit=False)
            for opcion in opciones:
                opcion.pregunta = pregunta
                opcion.save()
            return redirect('lista_preguntas')
    else:
        pregunta_form = PreguntaForm()
        formset = OpcionFormSet()
    return render(request, 'etica_app/crear_pregunta.html', {'pregunta_form': pregunta_form, 'formset': formset})


@user_passes_test(es_admin)
def editar_pregunta(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, id=pregunta_id)
    OpcionFormSet = inlineformset_factory(Pregunta, Opcion, form=OpcionForm, extra=0, can_delete=True)
    if request.method == 'POST':
        pregunta_form = PreguntaForm(request.POST, instance=pregunta)
        formset = OpcionFormSet(request.POST, instance=pregunta)
        if pregunta_form.is_valid() and formset.is_valid():
            pregunta_form.save()
            formset.save()
            return redirect('lista_preguntas')
    else:
        pregunta_form = PreguntaForm(instance=pregunta)
        formset = OpcionFormSet(instance=pregunta)
    return render(request, 'etica_app/editar_pregunta.html', {'pregunta_form': pregunta_form, 'formset': formset, 'pregunta': pregunta})


@user_passes_test(es_admin)
def eliminar_pregunta(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, id=pregunta_id)
    if request.method == 'POST':
        pregunta.delete()
        return redirect('lista_preguntas')
    return render(request, 'etica_app/eliminar_pregunta.html', {'pregunta': pregunta})


def ejercicios(request):
    preguntas = Pregunta.objects.all()

    if request.method == 'POST':
        puntaje = 0
        total_preguntas = preguntas.count()

        for pregunta in preguntas:
            opcion_id = request.POST.get(str(pregunta.id))
            if opcion_id:
                opcion_seleccionada = Opcion.objects.get(id=opcion_id)
                if opcion_seleccionada.es_correcta:
                    puntaje += 1

        porcentaje = int((puntaje / total_preguntas) * 100)

        fecha = timezone.now()


        return render(request, 'etica_app/resultado_examen.html', {
            'puntaje': puntaje,
            'total_preguntas': total_preguntas,
            'porcentaje': porcentaje,
            'fecha': fecha

        })
    else:
        return render(request, 'etica_app/ejercicios.html', {'preguntas': preguntas})

