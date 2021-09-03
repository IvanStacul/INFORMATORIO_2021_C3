# Django
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render
from django.http import HttpRequest

# Models
from django.contrib.auth.models import User
from apps.players.models import Player, Log

# Exception
from django.db.utils import IntegrityError


def login_player(request: HttpRequest):
    """Allows to authenticate a player."""

    if request.user.is_authenticated:
        return redirect('config')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        player = Player.objects.get(user_id=user.pk)
        if user:
            login(request, user)
            Log.objects.create(
                player=player,
                date=player.user.last_login
            )
            return redirect('config')
        else:
            return render(request, 'players/login.html', {'error': 'Usuario o contraseña incorrecta'})
    return render(request, 'players/login.html')


@login_required
def logout_player(request: HttpRequest):
    """Logout a player."""

    logout(request)
    return redirect('home')


def signup_player(request: HttpRequest):
    """Register new player."""

    if request.method == 'POST':

        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password != password_confirm:
            return render(
                request=request,
                template_name='players/signup.html',
                context={
                    'error': 'Las contraseñas no coinciden.'
                }
            )

        username = request.POST['username']
        email = request.POST['email']

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
        except IntegrityError:
            return render(
                request=request,
                template_name='players/signup.html',
                context={
                    'error': 'El usuario ingresado ya existe'
                }
            )

        # informacion adicional
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.is_staff = False
        user.is_superuser = False
        # import pdb; pdb.set_trace()
        user.save()

        player = Player(user=user)
        player.save()

        return redirect('login')

    return render(request=request, template_name='players/signup.html')
