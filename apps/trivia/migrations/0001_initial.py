# Generated by Django 3.2.6 on 2021-08-24 20:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('modified', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('created', models.DateTimeField(auto_now=True)),
                ('modified', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('start', models.DateTimeField(auto_now_add=True, verbose_name='Start')),
                ('end', models.DateTimeField(blank=True, null=True, verbose_name='End')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trivia.category')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trivia.level')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='players.player')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('modified', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trivia.category')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trivia.level')),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('isCorrect', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now=True)),
                ('modified', models.DateTimeField(auto_now_add=True)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trivia.level')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trivia.question')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isCorrect', models.BooleanField(default=False)),
                ('answered', models.BooleanField(default=False)),
                ('time', models.TimeField(null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trivia.question')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trivia.quiz')),
            ],
        ),
    ]