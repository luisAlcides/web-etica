from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contenido/<int:contenido_id>/', views.detalle_contenido, name='detalle_contenido'),
    path('ejercicios/', views.lista_ejercicios, name='lista_ejercicios'),
    path('temas/', views.lista_temas, name='lista_temas'),
    path('temas/crear/', views.crear_tema, name='crear_tema'),
    path('temas/<int:tema_id>/', views.detalle_tema, name='detalle_tema'),
    path('temas/<int:tema_id>/editar/', views.editar_tema, name='editar_tema'),
    path('temas/<int:tema_id>/eliminar/', views.eliminar_tema, name='eliminar_tema'),
]
