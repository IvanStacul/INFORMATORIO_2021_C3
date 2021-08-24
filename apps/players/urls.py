# Django
from django.urls import path

# Views
from . import views

urlpatterns = [
    path('login', views.login_player, name='login'),
]
