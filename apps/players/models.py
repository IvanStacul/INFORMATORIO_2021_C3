from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(
        upload_to='users/pictures',
        blank=True,
        null=True
    )
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Log(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
