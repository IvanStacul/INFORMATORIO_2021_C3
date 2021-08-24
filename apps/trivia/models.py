# Django
from django.db import models
from django.contrib.auth.models import User

# Models
from apps.players.models import Player


class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)
    created = models.DateTimeField(auto_now=True, auto_now_add=False)
    modified = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name


class Level(models.Model):
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now=True, auto_now_add=False)
    modified = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Question(models.Model):
    category = models.ForeignKey(
        Category, null=False, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, null=False, on_delete=models.CASCADE)
    content = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.content


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    isCorrect = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True, auto_now_add=False)
    modified = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self) -> str:
        return self.content


class Quiz(models.Model):
    category = models.ForeignKey(
        Category, null=False, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.IntegerField()
    start = models.DateTimeField(auto_now_add=True,
                                 verbose_name="Start")
    end = models.DateTimeField(null=True, blank=True, verbose_name="End")

    def __str__(self) -> str:
        return f"{self.category.name} - {self.level.name}"


class Game(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    isCorrect = models.BooleanField(default=False)
    answered = models.BooleanField(default=False)
    time = models.TimeField(null=True)

    def __str__(self) -> str:
        return f"{self.question.content} - {self.answered}"
