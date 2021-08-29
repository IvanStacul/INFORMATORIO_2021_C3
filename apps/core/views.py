# Django
from django.http.request import HttpRequest
from django.shortcuts import render

# Models
from apps.trivia.models import Quiz

def home(request: HttpRequest):
    return render(request, 'index.html')


def about(request: HttpRequest):
    return render(request, 'core/acerca_de.html')


def us(request):
    return render(request, 'core/creadores.html')


def contact(request):
    pass


def ranking(request: HttpRequest):

    quizzes = Quiz.objects.raw('SELECT MAX(score), * FROM trivia_quiz GROUP BY player_id')
    quizzes = sorted(quizzes, key=lambda q: (q.score, q.time()), reverse=False)
    return render(request, 'core/ranking.html', context={'quizzes': quizzes})
