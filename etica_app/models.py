from django.db import models

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