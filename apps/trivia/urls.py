# Django
from django.urls import path

# Views
from . import views

urlpatterns = [
    path('juego/<int:trivia>', views.play, name='play'),
    path('configuracion', views.config, name='config'),
    path('pregunta', views.pregunta, name='pregunta'),
]
