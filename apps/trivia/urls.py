# Django
from django.urls import path

# Views
from . import views

urlpatterns = [
    path('juego/<int:trivia>', views.play, name='play'),
    path('configuracion', views.config, name='config'),
    path('config', views.configuracion, name='configuracion'),
    path('pregunta', views.pregunta, name='pregunta'),
    path('sabias', views.sabias, name='sabias'),
    path('fin', views.fin, name='fin'),
]
