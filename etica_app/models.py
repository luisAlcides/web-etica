from django.db import models
from django.contrib.auth.models import User


class Contenido(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()

    def __str__(self):
        return self.titulo

class Ejercicio(models.Model):
    pregunta = models.TextField()
    respuesta_correcta = models.CharField(max_length=200)

    def __str__(self):
        return self.pregunta


class Tema(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['-creado_en']

class Pregunta(models.Model):
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE, related_name='preguntas')
    texto = models.TextField()

    def __str__(self):
        return self.texto

class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='opciones')
    texto = models.CharField(max_length=200)
    es_correcta = models.BooleanField(default=False)

    def __str__(self):
        return self.texto

class Resultado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    puntaje = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.tema.titulo} - {self.puntaje}'