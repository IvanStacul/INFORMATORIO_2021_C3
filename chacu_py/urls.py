from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jugador/', include('apps.players.urls')),
    path('trivia/', include('apps.trivia.urls')),
    path('', include('apps.core.urls')),
]
