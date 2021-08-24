# Django
from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseNotFound

# Models
from .models import Category, Game, Level, Question, Option, Quiz


@login_required
def play(request: HttpRequest, trivia: int):

    if not request.user.is_authenticated:
        return redirect('login')

    try:
        trivia = Quiz.objects.get(pk=trivia)
    except:
        return HttpResponseNotFound('El juego no existe')

    if not trivia.end is None:
        return render(
            request=request,
            template_name='trivia/play.html',
            context={
                'error': 'El juego ya finalizó.',
                'trivia': trivia,
            }
        )

    progress = Game.objects.filter(quiz_id=trivia.pk, answered=False).first()
    options = Option.objects.filter(
        question_id=progress.question.id,
        level_id=progress.quiz.level.id
    )

    if request.method == "POST":
        option_id = request.POST.get('answer')
        selected = Option.objects.get(pk=option_id)
        answer = Game.objects.get(question_id=request.POST.get('question_id'))

        answer.answered = True
        if selected.isCorrect:
            answer.isCorrect = True
            template_name = 'trivia/true.html'
            context = {
                'description': 'fue correcto',
                'trivia': trivia,
            }
        else:
            answer.isCorrect = False
            template_name = 'trivia/false.html'
            context = {
                'description': 'fue incorrecto',
                'trivia': trivia,
            }

        answer.save()

        if not Game.objects.filter(quiz_id=trivia.pk, answered=False).exists():
            quiz = Quiz.objects.get(pk=trivia.pk)
            quiz.end = timezone.now()
            quiz.save()

        return render(
            request=request,
            template_name=template_name,
            context=context
        )

    return render(
        request=request,
        template_name='trivia/play.html',
        context={
            'trivia': trivia.pk,
            'question': progress.question,
            'options': options
        }
    )


@login_required
def config(request: HttpRequest):

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
        ).order_by('?')[:2]

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

        # redirigir al juego
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
