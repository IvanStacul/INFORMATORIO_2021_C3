from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('chacu.py', views.about, name='about'),
    path('nosotros', views.us, name='us'),
    path('ranking', views.ranking, name='ranking'),
    path('contacto', views.contact, name='contact'),
]