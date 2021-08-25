# Django
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.http import HttpRequest


def login_player(request: HttpRequest):
    """Allows to authenticate a player."""

    if request.user.is_authenticated:
        return redirect('config')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('config')
        else:
            return render(request, 'players/login.html', {'error': 'Usuario o contraseña incorrecta'})
    return render(request, 'players/login.html')

@login_required
def logout_player(request: HttpRequest):
    """Logout a player."""
    
    logout(request)
    return redirect('home')
