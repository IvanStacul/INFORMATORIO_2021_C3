# Django
from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseNotFound
from django.conf import settings

# Models
from .models import Category, Game, Level, Question, Option, Quiz


@login_required
def play(request: HttpRequest, trivia: int):

    # si el usuario no esta logueado se redirecciona al login
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        # preguntamos si existe el juego que nos piden
        trivia = Quiz.objects.get(pk=trivia)
    except:
        # error 404
        return HttpResponseNotFound('El juego no existe')

    # si obtenemos una trivia pero ya finalizo lanzamos un error
    if not trivia.end is None:
        return render(
            request=request,
            template_name='trivia/play.html',
            context={
                'error': 'El juego ya finalizó.',
                'trivia': trivia,
                'max_score': settings.QUESTION_LIMIT * 20
            }
        )

    # obtenemos la primer pregunta no respondida del juego en progreso
    progress = Game.objects.filter(quiz_id=trivia.pk, answered=False).first()
    # luego extraemos las opciones a esa pregunta
    options = Option.objects.filter(
        question_id=progress.question.id,
        level_id=progress.quiz.level.id
    )

    # si ya se envio una respuesta a la pregunta
    if request.method == "POST":

        selected = Option.objects.get(  # opcion elegida
            pk=request.POST.get('answer')
        )
        answer = Game.objects.get(  # pregunta que se respondio
            question_id=request.POST.get('question_id'),
            quiz_id=trivia.pk
        )

        answer.answered = True  # marcar como respondida la pregunta

        if selected.isCorrect:  # si la opcion elegida es la correcta
            answer.isCorrect = True  # marcar como acertada la pregunta
            template_name = 'trivia/true.html'  # devolver una pagina de acierto
            context = {
                'description': 'fue correcto',
                'trivia': trivia,
            }
        else:
            answer.isCorrect = False  # marcar como erronea la pregunta
            template_name = 'trivia/false.html'
            context = {
                'description': 'fue incorrecto',
                'trivia': trivia,
            }

        answer.save()  # guardar resultados de la pregunta

        game = Game.objects.filter(quiz_id=trivia.pk)

        # si ya no existen mas preguntas por responder
        if not game.filter(answered=False).exists():
            quiz = Quiz.objects.get(pk=trivia.pk)  # obtener el quiz actual
            quiz.score = len(game.filter(isCorrect=True)) * 20
            quiz.end = timezone.now()  # guardar el tiempo de fin del quiz
            quiz.save()  # guardar resultados

        # renderea la pagina de resultado de la opcion elegida
        return render(
            request=request,
            template_name=template_name,
            context=context
        )

    # renderea el juego con las preguntas y opciones
    return render(
        request=request,
        template_name='trivia/play.html',
        context={
            'trivia': trivia.pk,
            'question': progress.question,
            'options': options,
        }
    )


@login_required
def config(request: HttpRequest):

    # si el usuario no esta logueado se redirecciona al login
    if not request.user.is_authenticated:
        return redirect('login')

    # si el formulario fue enviado
    if request.method == 'POST':
        # comprueba si se enviaron el nivel y categoría
        try:
            category = request.POST['category']
            level = request.POST['level']
        except:
            return render(
                request=request,
                template_name='trivia/error.html',
                context={
                    'description': 'No se configuró ninguna partida'
                }
            )

        # elegir las preguntas que participan en la trivia
        questions = Question.objects.filter(
            category_id=1,
            level_id=1
        ).order_by('?')[:settings.QUESTION_LIMIT]

        # si no hay preguntar para elegir enviamos un error
        if not questions.exists():
            return render(
                request=request,
                template_name='trivia/error.html',
                context={
                    'description': 'No se pudo crear la partida porque no exiten preguntas de la categoría y/o nivel elegido'
                }
            )

        # crear un juego
        quiz = Quiz.objects.create(
            score=0,
            category_id=category,
            level_id=level,
            player_id=request.user.player.id,
            user_id=request.user.id,
        )

        # guardar el progreso del juego
        for question in questions:
            Game.objects.create(
                quiz_id=quiz.pk,
                question_id=question.pk,
            )

        # redirigir al juego para comenzar la partida
        return redirect('play', trivia=quiz.id)

    # Buscamos si exite un juego en progreso
    trivia = Quiz.objects.filter(player_id=request.user.player.id).last()

    # si el juego esta en progreso lo redirigimos para que siga jugando
    if not trivia is None:
        if trivia.end is None:
            return redirect('play', trivia=trivia.pk)

    # renderea la página de configuración
    return render(
        request=request,
        template_name='trivia/config.html',
        context={
            'levels': Level.objects.all(),
            'categories': Category.objects.all(),
        }
    )
