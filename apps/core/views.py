# Django
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.core import serializers

# Models
from apps.trivia.models import Category, Level, Option, Question, Quiz
from apps.players.models import Log, Player

from datetime import date, datetime


def home(request: HttpRequest):
    return render(request, 'index.html')


def about(request: HttpRequest):
    return render(request, 'core/acerca_de.html')


def us(request):
    return render(request, 'core/creadores.html')


def contact(request):
    pass


def ranking(request: HttpRequest):
    qid = []
    # players id
    pid=Quiz.objects.values('player_id').distinct()
    for pi in pid:
        qs = Quiz.objects.filter(player_id=pi['player_id'])
        qs = sorted(qs, key=lambda q: (q.score, q.time()), reverse=True)
        qid.append(qs[0].id)
    quizzes = Quiz.objects.filter(pk__in=qid)
    return render(request, 'core/ranking.html', context={'quizzes': quizzes})


def pivot_data(request: HttpRequest):
    dates = []
    values = []

    if request.GET.get('chart') == 'games':
        data = Quiz.objects.raw(
            'SELECT COUNT(*) AS "RESULT", DATE("end") AS "END", id FROM trivia_quiz GROUP BY DATE("end")')
        for d in data:
            dates.append(d.END)
            values.append(d.RESULT)
    if request.GET.get('chart') == 'logs':
        data = Log.objects.raw(
            'SELECT COUNT(*) AS "RESULT", DATE("date") AS "DATE", pl.id FROM players_log pl GROUP BY DATE("date")')
        for d in data:
            dates.append(d.DATE)
            values.append(d.RESULT)

    data = {
        'dates': dates[-6:],
        'values': values,
    }

    return JsonResponse(data, safe=False)


@login_required
def admin_panel(request: HttpRequest):
    context = {
        'players_count': Player.objects.count(),
        'quiz_count': Quiz.objects.count(),
    }
    return render(request, 'core/admin/panel.html', context)


@login_required
def trivia_config(request: HttpRequest):
    context = {
        'status': '',
        'error': '',
        'levels': Level.objects.all(),
        'categories': Category.objects.all(),
    }
    if request.method == 'POST':
        category = request.POST.get('category')
        category_id = request.POST.get('category_id')
        level = request.POST.get('level')
        level_id = request.POST.get('level_id')
        if category:
            Category.objects.create(name=category)
            context['status'] = 'Categoría creada con éxito'
        if category_id:
            Category.objects.filter(pk=category_id).delete()
        if level:
            Level.objects.create(name=level)
            context['status'] = 'Nivel creada con éxito'
        if level_id:
            Level.objects.filter(pk=level_id).delete()
        return redirect('trivia_config')
    return render(request, 'core/admin/configuration.html', context)


@login_required
def trivia_questions(request: HttpRequest):
    context = {
        'status': '',
        'error': '',
        'levels': Level.objects.all(),
        'categories': Category.objects.all(),
        'questions': Question.objects.all(),
    }
    if request.method == 'POST':
        question_id = request.POST.get('question_id')

        data = {
            'level_id': request.POST.get('level_id'),
            'category_id': request.POST.get('category_id'),
            'content': request.POST.get('content'),
            'description': request.POST.get('description'),
        }

        if not all(value == None for value in data.values()):
            Question.objects.create(**data)
            return redirect('trivia_questions')

        if question_id:
            Question.objects.filter(pk=question_id).delete()
            context['status'] = 'Categoría borrada con éxito'
            return redirect('trivia_questions')

    return render(request, 'core/admin/questions/index.html', context)


@login_required
def trivia_question_edit(request: HttpRequest, question_id: int):
    context = {
        'status': '',
        'error': '',
        'levels': Level.objects.all(),
        'categories': Category.objects.all(),
        'questions': Question.objects.all(),
        'question_edit': Question.objects.get(pk=question_id),
    }
    if request.method == 'POST':
        data = {
            'level_id': request.POST.get('level_id'),
            'category_id': request.POST.get('category_id'),
            'content': request.POST.get('content'),
            'description': request.POST.get('description'),
        }

        Question.objects.filter(pk=question_id).update(**data)

        return redirect('trivia_questions')

    return render(request, 'core/admin/questions/edit.html', context)


@login_required
def trivia_options(request: HttpRequest):
    context = {
        'status': '',
        'error': '',
        'levels': Level.objects.all(),
        'options': Option.objects.all(),
        'questions': Question.objects.all(),
    }

    if request.method == 'POST':
        option_id = request.POST.get('option_id')

        data = {
            'level_id': request.POST.get('level_id'),
            'question_id': request.POST.get('question_id'),
            'content': request.POST.get('content'),
            'isCorrect': None,
        }

        if not all(value is None for value in data.values()):
            if request.POST.get('isCorrect') is 'on':
                isCorrect = True
            else:
                isCorrect = False
            data['isCorrect'] = isCorrect
            Option.objects.create(**data)
            return redirect('trivia_options')

        if option_id:
            Option.objects.filter(pk=option_id).delete()
            context['status'] = 'Opción borrada con éxito.'
            return redirect('trivia_options')

    return render(request, 'core/admin/options/index.html', context)


@login_required
def trivia_option_edit(request: HttpRequest, option_id: int):
    context = {
        'status': '',
        'error': '',
        'levels': Level.objects.all(),
        'options': Option.objects.all(),
        'option_edit': Option.objects.get(pk=option_id),
        'questions': Question.objects.all(),
    }

    if request.method == 'POST':
        if request.POST.get('isCorrect') is 'on':
            isCorrect = True
        else:
            isCorrect = False

        data = {
            'level_id': request.POST.get('level_id'),
            'question_id': request.POST.get('question_id'),
            'content': request.POST.get('content'),
            'isCorrect': isCorrect,
        }

        data['isCorrect'] = isCorrect
        Option.objects.filter(pk=option_id).update(**data)
        return redirect('trivia_options')

    return render(request, 'core/admin/options/edit.html', context)
